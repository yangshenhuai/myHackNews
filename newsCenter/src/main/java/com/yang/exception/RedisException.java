package com.yang.exception;

/**
 * Created by yangshenhuai on 16-2-2.
 */
public class RedisException extends RuntimeException {

    public String reason;

    public RedisException(String reason) {
        super(reason);
        this.reason = reason;
    }
}
