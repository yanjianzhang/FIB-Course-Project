
library(readr)
raw_data <- read_delim("dict/Merge_Apify_Reviews_Spark_tfidf.csv",
                       delim = ";", escape_double = FALSE, trim_ws = TRUE, show_col_types = FALSE)

# Dataset extracted from: https://data.world/kgarrett/whats-on-the-menu/workspace/query?queryid=5d1d1edb-5e6c-4bc7-bf9e-b128f846b959
library(dplyr)
dictionary <- read_csv("dict/dictionary.csv", show_col_types = FALSE) %>%
              mutate(food = tolower(name)) %>% select(-name)

type_cuisine <- read_csv("dict/type_cuisine.csv", show_col_types = FALSE) %>%
                         mutate(cuisine = tolower(cuisine)) %>% distinct(cuisine)

options(scipen=999)
library(tidyr)
library(stringr)
data <- raw_data %>% select(-c(title, text, biz_id)) %>% 
                     rename(unique_id = `...1`) %>%
                     drop_na(reviewerId, biz_name) %>%
                     filter(!str_detect(reviewerId,'\\s')) %>%
                     distinct(merge_id, reviewerId, .keep_all = TRUE) %>%
                     mutate(rest_name = gsub('"', '', biz_name)) %>%
                     select(-biz_name) %>% rename(biz_name = rest_name)
rm(raw_data)

establishments <- data %>% distinct(merge_id,biz_name)

user_likes_establishment <- data %>% filter(rating == 5) %>% select(reviewerId, merge_id)

users <- data %>% distinct(reviewerId)

food_tags <- data %>% select(food, merge_id, reviewerId) %>% drop_na() %>% 
                      mutate(tags = strsplit(as.character(food), ",")) %>%
                      unnest(tags) %>% mutate(food = tolower(tags)) %>%
                      left_join(dictionary, by = c("food" = "food")) %>% 
                      drop_na() %>% select(merge_id, reviewerId, food)

temp <- food_tags %>% distinct(food) %>% 
        filter(!food %in% c('fresh', 'sparkling', 'dressing', 'sage')) %>% filter(!(!(str_detect(food,'\\s'))&(str_detect(food,'ed'))))


library(stringi)
set.seed(123)
tag_id <- do.call(paste0, Map(stri_rand_strings, n=nrow(temp), length=c(2, 2, 2, 2, 2),
                              pattern = c('[A-Z]', '[0-9]', '[a-z]', '[0-9]', '[a-z]')))

food <- as.data.frame(cbind(tag_id, temp)) 

establishment_offers_food <- inner_join(food, food_tags, by = "food") %>% distinct(merge_id, tag_id)

user_likes_food <- left_join(user_likes_establishment, food_tags, by=c('reviewerId'='reviewerId', 'merge_id'='merge_id')) %>% 
                   drop_na() %>% distinct() %>% inner_join(food, by = "food") %>% distinct(reviewerId, tag_id) 

# Cuisine
set.seed(123)
cuisine_id <- do.call(paste0, Map(stri_rand_strings, n=nrow(type_cuisine), length=c(1, 1, 1, 1, 1),
                                  pattern = c('[A-Z]', '[0-9]', '[a-z]', '[0-9]', '[a-z]')))

type_cuisine <- as.data.frame(cbind(cuisine_id, type_cuisine)) 


environment_tags <- data %>% select(merge_id, reviewerId, food, phrase, tfidf) %>% 
                    unite("temp", food:phrase, sep= ",") %>% unite("tags", temp:tfidf, sep= ",") %>% 
                    mutate(temp = str_remove_all(tags, 'NA,'), temp = str_replace_all(temp,',,',','), tags = strsplit(as.character(temp), ",")) %>%
                    select(-temp) %>% unnest(tags) 

establishment_has_cuisine <- inner_join(environment_tags, type_cuisine, by = c('tags' = 'cuisine')) %>%
                             group_by(merge_id, .drop = FALSE) %>% count(tags) %>% filter(n >= 3) %>% 
                             left_join(type_cuisine, by=c('tags'='cuisine')) %>% select(merge_id, cuisine_id)

type_cuisine <- type_cuisine %>% filter(cuisine_id %in% establishment_has_cuisine$cuisine_id)


atmosphere <- c('casual', 'relaxed', 'romantic', 'pricey', 'elegant', 'attentive', 'friendly staff', 'original', 'beautiful view', 'beautiful views', 
                 'welcoming', 'quiet', 'loud music', 'crowdy', 'noisy', 'gourmet', 'michelin star', 'michelin stars', 'modern', 'stylish', 'vegan', 'live music',
                 'friends', 'family', 'kids', 'tasting menu', 'party', 'nicely decorated', 'vegetarian option', 'gluten free')
atmosphere_id <- 1:30

atmosphere <- as.data.frame(cbind(atmosphere_id, atmosphere)) 

establishment_has_atmosphere <- inner_join(environment_tags, atmosphere, by=c('tags'='atmosphere'), copy=TRUE) %>%
                                group_by(merge_id, .drop = FALSE) %>% count(atmosphere_id) %>% filter(n >= 3) %>% select(-n)

temp <- inner_join(environment_tags, atmosphere, by=c('tags'='atmosphere'), copy=TRUE)
user_wants_atmosphere <- left_join(user_likes_establishment, temp, by=c('reviewerId'='reviewerId', 'merge_id'='merge_id')) %>% 
                         drop_na() %>% select(reviewerId, atmosphere_id)
            

set.seed(123)
# Assign friends
friend1<-c()
friend2<-c()
for(i in 1:100000){
  temp1 <- sample(1:nrow(users),1)
  temp2 <- sample(1:nrow(users),1)
  if(temp1 == temp2){temp1=temp1+1}
  friend1 <- c(friend1, users$reviewerId[temp1])
  friend2 <- c(friend2, users$reviewerId[temp2])
}
user_isFriendsWith <- as.data.frame(cbind(friend1,friend2)) 



## READY ##

setwd("C:/Users/marit/OneDrive - Universit� Libre de Bruxelles/Bureau/BDMA/UPC/SDM/Project/Files")

myList <- list(establishments = establishments,
               user_likes_establishment = user_likes_establishment,
               food = food,
               establishment_offers_food = establishment_offers_food,
               user_likes_food = user_likes_food,
               establishment_has_cuisine = establishment_has_cuisine,
               type_cuisine = type_cuisine,
               establishment_has_atmosphere = establishment_has_atmosphere,
               user_wants_atmosphere = user_wants_atmosphere,
               user_isFriendsWith = user_isFriendsWith,
               atmosphere = atmosphere,
               users = users)

invisible(mapply(write_csv, myList, file=paste0(names(myList), '.csv')))
