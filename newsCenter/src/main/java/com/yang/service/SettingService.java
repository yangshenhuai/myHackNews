package com.yang.service;

import com.yang.bean.Setting;
import com.yang.exception.RedisException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.ListOperations;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.data.redis.core.SetOperations;
import org.springframework.stereotype.Service;
import org.springframework.util.MultiValueMap;
import org.springframework.util.StringUtils;

import java.util.*;

/**
 * Created by yangshenhuai on 16-2-1.
 */
@Service
public class SettingService {


    public static final String URLS_KEY = "urls";
    public static final String URL_DELIMETER = ":";
    public static final String KEYWORD_DELIMETER = ",";

    private RedisTemplate<String,String> redisTemplate;



    @Autowired
    public SettingService(RedisTemplate<String,String> redisTemplate){
        this.redisTemplate = redisTemplate;
    }


    public Map<String,String> getUrlMaps(){
        List<String> urls = redisTemplate.opsForList().range(URLS_KEY, 0, -1);

        Map<String,String> result = new HashMap<String,String>();
        urls.stream().map( url-> url.split(":")).forEach(arr-> result.put(arr[0],arr[1]));
        return result;
    }


    public void updateSettings(MultiValueMap<String, String> map) {
        System.out.println("map -----" + map);
        SetOperations<String,String> setOperations = redisTemplate.opsForSet();
        map.entrySet().stream().forEach(entry->{
                    try {
                        redisTemplate.delete(entry.getKey());
                        if (entry.getValue() != null && !entry.getValue().isEmpty()){
                            setOperations.add(entry.getKey(),entry.getValue().get(0).split(","));
                        }
                    }catch (Throwable t) {
                        System.err.println("fail to update redis");
                        throw new RedisException("fail to update settings");
                    }

           }
        );



    }


    public void updateSettings(List<Setting> settings) {
        redisTemplate.delete(URLS_KEY); // delete urls key
        redisTemplate.execute(redisConnection->{
            redisConnection.del(URLS_KEY.getBytes());
            settings.forEach(setting->{
                if (!StringUtils.isEmpty(setting.getName()) && !StringUtils.isEmpty(setting.getUrl())) {
                    redisConnection.lPush(URLS_KEY.getBytes(), (setting.getName() + URL_DELIMETER + setting.getUrl()).getBytes());
                }
                if (!StringUtils.isEmpty(setting.getName()) && !StringUtils.isEmpty(setting.getKeyWords())){
                    redisConnection.del(setting.getName().getBytes());
                    for (String keyword : setting.getKeyWords().split(KEYWORD_DELIMETER)){
                        redisConnection.sAdd(setting.getName().getBytes(),keyword.getBytes());
                    }

                }
            });
            return null;
        },false,true);


    }



    public Map<String, String> getUrlKeyWords(Optional<Map<String, String>> urlMap) {
        Map<String,String> result = new HashMap<String,String>();
        SetOperations<String,String> setOperations = redisTemplate.opsForSet();
        urlMap.ifPresent(
                map -> {

                    map.forEach((String key, String value) -> {
                        Set members = setOperations.members(key);
                        String keyWordStr = String.join(",", members);
                        result.put(key, keyWordStr);
                    });


                }
        );
        return result;


    }

    public List<Setting> getSettings() {

        Map<String,String> urlMap = getUrlMaps();
        Map<String,String> urlKeywords = getUrlKeyWords(Optional.of(urlMap));

       List<Setting> resultList = new ArrayList<Setting>();
        urlMap.forEach(
                (String name,String url)->{
                    String keyWords = urlKeywords.get(name);
                    resultList.add(new Setting(name,url,keyWords));
                }
        );
        return resultList;
    }
}
