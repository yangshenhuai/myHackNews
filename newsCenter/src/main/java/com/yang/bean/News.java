package com.yang.bean;

/**
 * Created by yangshenhuai on 16-2-14.
 */
public class News {

    private String title;

    private String url;

    private long captureTimeStamp;

    public News() {
    }

    public News(String title, String url) {
        this.title = title;
        this.url = url;
    }

    public News(String title, String url, long captureTimeStamp) {
        this.title = title;
        this.url = url;
        this.captureTimeStamp = captureTimeStamp;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public long getCaptureTimeStamp() {
        return captureTimeStamp;
    }

    public void setCaptureTimeStamp(long captureTimeStamp) {
        this.captureTimeStamp = captureTimeStamp;
    }
}
