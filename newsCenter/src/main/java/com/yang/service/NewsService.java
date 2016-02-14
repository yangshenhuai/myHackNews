package com.yang.service;

import com.yang.bean.News;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.ZSetOperations;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * Created by yangshenhuai on 16-2-14.
 */
@Service
public class NewsService {

    private static final String RESULT_TABLE = "result_table";
    private static final String DELEMETER = "@@";

    private RedisTemplate<String,String> redisTemplate;

    @Autowired
    public NewsService(RedisTemplate<String,String> redisTemplate){
        this.redisTemplate = redisTemplate;
    }


    public List<News> getNews(){

        ZSetOperations<String, String> zSetOperations = redisTemplate.opsForZSet();

        Set<String> results = zSetOperations.reverseRange(RESULT_TABLE,0, -1);
        List<News> news = new ArrayList<News>();
        results.stream().forEach(resultStr->{
            String[] resultArr = resultStr.split(DELEMETER);
            if (resultArr.length == 2 && resultArr[1].startsWith("http")) {
                news.add(new News(resultArr[0],resultArr[1]));
            }
        });

        return news;

    }


}
