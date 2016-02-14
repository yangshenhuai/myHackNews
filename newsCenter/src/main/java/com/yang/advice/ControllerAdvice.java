package com.yang.advice;

import com.yang.exception.RedisException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.ExceptionHandler;

/**
 * Created by yangshenhuai on 16-2-2.
 */
@org.springframework.web.bind.annotation.ControllerAdvice
public class ControllerAdvice {


    private Logger logger = LoggerFactory.getLogger(ControllerAdvice.class);



    @ExceptionHandler(RedisException.class)
    public String redisException(){
        return "redisException";
    }





}
