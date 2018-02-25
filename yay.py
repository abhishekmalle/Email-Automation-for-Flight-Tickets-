'''
title: 'NLP analysis on the SOTU addresses'
author: "Jonathan Bouchet"
date: "`r Sys.Date()`"
output:
 html_document:
    fig_width: 10
    fig_height: 7
    toc: yes
    number_sections : yes
    code_folding: show
'''

<center><img src="http://america.aljazeera.com/content/ajam/topics/topic/event/state-of-the-union-2014/jcr:content/targetParsys/adaptiveimage/src.adapt.960.high.SOTU_WEB%20BANNER%20960X252.1391017788247.jpg"></center>

```{r setup}
options(width=100)
knitr::opts_chunk$set(out.width='1000px',dpi=200,message=FALSE,warning=FALSE)
```

```{r}
#load packages and csv file
library(ggplot2)
library(dplyr)
library(gridExtra)
library(RColorBrewer)
library(ggthemes)
library(ggrepel)
library(tm)
library(wordcloud)
library(tidytext)
library(lsa)
library(corrplot)
```

#Motivation
As Rachael Tatman mentioned in the descripion, there is a lot to look at with these data.

I will be looking/doing at :

* clustering addresses and see if one can find clusters by `president`, `party`
* wordclouds by `president`, `party`
* word frequency by `time`, `president`, `party`

#Corpus preparation

* load all texts as a Corpus of 29 documents
* remove numbers, punctuation, stopwords and whitespaces
```{r}
docs<-Corpus(DirSource("../input/"))
docs_clean <- docs %>%
  tm_map(content_transformer(tolower)) %>%
  tm_map(content_transformer(removeNumbers)) %>%
  tm_map(content_transformer(removePunctuation)) %>%
  tm_map(content_transformer(removeWords),tidytext::stop_words$word) %>%
  tm_map(content_transformer(trimws)) %>%
  tm_map(content_transformer(stripWhitespace))
m_docs_clean<-TermDocumentMatrix(docs_clean)
```

#Clusters

* apply a SVD dimensionality reduction, using `share` : a fraction of the sum of the selected singular values to the sum of all singular values (default: 0.5)
* select the 2 first PCA for plotting

```{r}
lsa_out <- lsa::lsa(m_docs_clean, dims = lsa::dimcalc_share())
docs_mat<- lsa_out$dk[,c(1:2)]
docs_mat_df<- as.data.frame(docs_mat)
colnames(docs_mat_df)<-c("dim1", "dim2")
```

As there are 5 differents presidents, a _natural_ number of clusters to find is 5.

```{r}
set.seed(1234)
# 5 different presidents
clus<-kmeans(docs_mat_df,5)
docs_mat_df$cluster<-factor(clus$cluster)
ggplot(data=docs_mat_df,aes(x=dim1,y=dim2)) +
  geom_point(aes(color=cluster),size=2) +
  geom_abline(slope=-4,intercept=-.55,alpha=.5,lty=2) +
  geom_label_repel(aes(label=rownames(docs_mat_df)),data=docs_mat_df,size=3) +
  theme_fivethirtyeight() +
  scale_color_brewer(palette='Set1')
```

* I draw the dashline myself by observation of a clusterisation by party (minus `Bush-1992`)
* Obama's speeches are pretty well clustered
* Clinton's speeches(1993 to 1995) are also well clustered
* G. W. Bush's speeches(2002 to 2008) are well clustered
* so it seems that Trump is closer to Republicans than Democrats
* `Bush-2001` is close to `Bush-1989, Bush-1990, Bush-1991` ? Does it mean G. W. Bush took inspiration from his father ... ?

#Words analysis
##Code

* Same Corpus filtering as in `Section-1`.
* decode the president's name, party and year of activity from the name of the file.
* append everything in a dataframe.

```{r}
makeFrequencyWord<-function(df){
  temp<-Corpus(VectorSource(df[,]))
  temp_clean <- temp %>%
  tm_map(content_transformer(tolower)) %>%
  tm_map(content_transformer(removeNumbers)) %>%
  tm_map(content_transformer(removePunctuation)) %>%
  tm_map(content_transformer(removeWords),tidytext::stop_words$word) %>%
  tm_map(content_transformer(trimws)) %>%
  tm_map(content_transformer(stripWhitespace))

  word_Vec<-c()
  for (i in 1:length(temp_clean)){
    current<-sort(strsplit(as.character(temp_clean[[i]]$content),' ')[[1]])
    word_Vec<-append(word_Vec,current,length(current))
  }
    return(word_Vec)
}


files <- list.files(path="../input", pattern="*.txt", full.names=T, recursive=FALSE)
listAll<-list()
for(i in 1:length(files)){
    dat<-as.data.frame(readLines(files[i]),stringsAsFactors=F)
    president<-strsplit(gsub("../input/|.txt","",files[i]),'_')[[1]][1]
    year<-as.numeric(strsplit(gsub("../input|.txt","",files[i]),'_')[[1]][2])

    dat_words<-makeFrequencyWord(dat)

    dat_df<-data.frame('word'= dat_words)
    dat_df$year<-rep.int(year,nrow(dat_df))

    if(president=='Bush'){
        if(year<2001){
            president<-paste0(president,'-Sr')
            }
            else {
                president<-paste0(president,'-Jr')
            }
        }

    dat_df$president<-rep(president,nrow(dat_df))
    if(president %in% c('Bush-Sr','Bush-Jr','Trump')){
        dat_df$party<-rep('Republican',nrow(dat_df))
    }
    else{
            dat_df$party<-rep('Democrat',nrow(dat_df))
        }
    listAll[[i]]<-dat_df
}

RES <- do.call("rbind", listAll)
```

##Distributions of the 30 most frequents words

```{r}
presidents<-c('Bush-Sr','Clinton','Bush-Jr','Obama','Trump')
wordPresident<-list()
for(i in 1:length(presidents)){
  col<-ifelse(i %in% c(2,4),'Blues','Reds')
  wordPresident[[i]]<-RES %>%
    filter(president==presidents[i]) %>%
    group_by(word) %>%
    summarise(count=n()) %>%
    top_n(30) %>%
    ggplot(aes(x=reorder(word,count),y=count,fill=count)) +
    geom_histogram(stat='identity') +
    coord_flip() +
    theme_fivethirtyeight() +
    ggtitle(paste0('Most frequent words used by ',presidents[i])) +
    theme(legend.position='none',
          plot.title = element_text(size =10),
          axis.text = element_text(size=10)) +
    scale_fill_gradientn(colors=brewer.pal(2,col))
}
```

```{r fig.width=10, fig.height=15, fig.align='center',eval=T}
do.call(grid.arrange, c(wordPresident, ncol=2))
```

##Word Clouds
```{r fig.width=10, fig.height=15, fig.align='center',eval=T}
set.seed(1234)
par(mfrow=c(3, 2),bg="black")
for(i in 1:length(presidents)){
    tdm <- TermDocumentMatrix(Corpus(VectorSource((RES %>% filter(president==presidents[i]) %>% select(word))$word)))
    m_tdm<-as.matrix(tdm)
    word.freq<-sort(rowSums(m_tdm), decreasing=T)
    col<-ifelse(i %in% c(2,4),'Blues','Reds')
    pal<-rev(brewer.pal(10,col))
    wordcloud(words=names(word.freq),freq = word.freq,random.order=F,colors=pal, max.words=200,scale=c(3,1))
    title(paste0('Most frequent words used by ',presidents[i]),col.main='#EBCC2A',cex.main=1.25)
}
```

#Counts vs. Time
We see from the different `wordcloud` that a word can have variations (mainly because of the `stemming` missing step) :
```{r}
RES %>% group_by(word) %>% summarize(count=n()) %>% filter(grepl("^america",word))
```

So instead a searching for 1 word and missing the others, we can search for a group of word (`theme`)

##`AMERICA` and variant
```{r}
am<-c('america','american','americas','americans')
tt<-data.frame(word=character(), year=integer(), president = character(), party=character())
for(j in 1:length(listAll)){
  temp<-listAll[[j]] %>% filter(word %in% am)
  tt<-rbind(tt,temp)
}
#head(tt)
```

```{r}
#define rectangle for colors
start_r<-c(1988.5,2000.5,2016.5)
end_r<-c(1992.5,2008.5,2017.5)
dates_r<-data.frame(xmin=start_r,xmax=end_r,ymin=0,ymax=Inf)

start_b<-c(1992.5,2008.5)
end_b<-c(2000.5,2016.5)
dates_b<-data.frame(xmin=start_b,xmax=end_b,ymin=0,ymax=Inf)

colfunc <- colorRampPalette(c("black", "gray"))
```

```{r}
tt %>% group_by(year,word) %>%
  summarize(count=n()) %>%
  ggplot() + geom_bar(aes(x=year,y=count,fill=word),stat='identity',alpha=1) +
  theme_fivethirtyeight() +
  scale_fill_manual(name="",values = colfunc(length(unique(tt$word)))) +
  geom_rect(data = dates_r, aes(xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax), alpha = 0.3,fill='red') +
  geom_rect(data = dates_b, aes(xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax), alpha = 0.3,fill='blue') +
  ggtitle('Counts of \"America\" and its variants')
```

##`TAX` and its variants
```{r}
alltax<-c('tax','taxes','taxpayer','taxpayers')
tt<-data.frame(word=character(), year=integer(), president = character(), party=character())
for(j in 1:length(listAll)){
  temp<-listAll[[j]] %>% filter(word %in% alltax)
  tt<-rbind(tt,temp)
}
```

```{r}
tt %>% group_by(year,word) %>%
  summarize(count=n()) %>%
  ggplot() + geom_bar(aes(x=year,y=count,fill=word),stat='identity',alpha=1) +
  theme_fivethirtyeight() +
  scale_fill_manual(name="",values = colfunc(length(unique(tt$word)))) +
  geom_rect(data = dates_r, aes(xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax), alpha = 0.3,fill='red') +
  geom_rect(data = dates_b, aes(xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax), alpha = 0.3,fill='blue') +
  ggtitle('Counts of \"Tax\" and its variants')
```

##`JOB` and its variants
```{r}
alljob<-c('job','jobs')
tt<-data.frame(word=character(), year=integer(), president = character(), party=character())
for(j in 1:length(listAll)){
  temp<-listAll[[j]] %>% filter(word %in% alljob)
  tt<-rbind(tt,temp)
}
```

```{r}
tt %>% group_by(year,word) %>%
  summarize(count=n()) %>%
  ggplot() + geom_bar(aes(x=year,y=count,fill=word),stat='identity',alpha=1) +
  theme_fivethirtyeight() +
  scale_fill_manual(name="",values = colfunc(length(unique(tt$word)))) +
  geom_rect(data = dates_r, aes(xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax), alpha = 0.3,fill='red') +
  geom_rect(data = dates_b, aes(xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax), alpha = 0.3,fill='blue') +
  ggtitle('Counts of \"Job\" and its variants')
```

* `AMERICA` and its variant looks a theme more addressed by Democrats
* `TAX` is also a word mostly addressed by Democrats ; the fall from 20 to 5 during the first Bush-Jr is also strange.
* `JOB` theme seems a subject of matter more addressed by Democrats than Republican.
* for all these themes, it's interesting to see the changes each time Democrats/Republicans switch

<hr>
<strong>History :</strong>

* _version 1 : initial commit_
* _version 2 : added word count per year_
* _version 3 : replaced word-count by theme-count per year_

<hr>
