package com.yang.bean;

/**
 * Created by yangshenhuai on 16-2-2.
 */
public class Setting {

    private String name;

    private String url;

    private String keyWords;

    public Setting() {
    }

    public Setting(String name, String url, String keyWords) {
        this.name = name;
        this.url = url;
        this.keyWords = keyWords;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getKeyWords() {
        return keyWords;
    }

    public void setKeyWords(String keyWords) {
        this.keyWords = keyWords;
    }
}
