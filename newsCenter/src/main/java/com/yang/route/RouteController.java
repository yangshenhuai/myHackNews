package com.yang.route;

import com.yang.bean.News;
import com.yang.bean.Setting;
import com.yang.common.Response;
import com.yang.service.NewsService;
import com.yang.service.SettingService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.util.MimeType;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.List;


/**
 * Created by yangshenhuai on 16-1-31.
 */
@Controller
public class RouteController {

    private static final Logger logger = LoggerFactory.getLogger(RouteController.class);

    private SettingService settingService;
    private NewsService newsService;

    @RequestMapping("/settings")
    public String settings(Model model){

        model.addAttribute("settings",settingService.getSettings());

        return "settings";
    }


    @RequestMapping(value = "/settings/update" ,method = RequestMethod.POST,produces ="application/json",consumes = "application/json")
    @ResponseBody
    public int updateSettings(@RequestBody List<Setting> settings){
        try{
            settingService.updateSettings(settings);
            return Response.SUCCESS;

        } catch (Throwable t){
            logger.error("fail to update settings " ,t.getMessage());
            return Response.FAIL;

        }
    }


    @RequestMapping("/")
    public String index(Model model){
        List<News> newsList = newsService.getNews();
        model.addAttribute("newsList",newsList);

        return "index";
    }

    @Autowired
    public void setSettingService(SettingService settingService) {
        this.settingService = settingService;
    }
    @Autowired
    public void setNewsService(NewsService newsService) {
        this.newsService = newsService;
    }
}
