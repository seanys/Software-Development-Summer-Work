<?php
defined('BASEPATH') or exit('No direct script access allowed');
header('Access-Control-Allow-Origin:*');    
header('Access-Control-Allow-Methods:*');  
//header('Access-Control-Allow-Headers:x-requested-with,content-type');   
use QCloud_WeApp_SDK\Mysql\Mysql as DB;//数据库连接，按照config中链接

class Article extends CI_Controller
{
    //主函数部分
    public function index()
    {
        if (($_GET['article_id'])){
            $article=DB::row('articles',['*'],"id=".$_GET['article_id']);
            $article_detail=DB::select('article_content',['*'],"article_id=".$_GET['article_id']);
	        if(count($article)>0){
                $city=DB::row('places',['*'],"name='".$article->place."'");
                $this->json([
                    'code' => 1,
                    'data' => [
                        "article"=>$article,
                        "article_detail" => $article_detail,
                        "city"=>$city
                    ],
                ]);
            }
            else{
                $this->json([
                    'code' => 0
                ]);
            }
        }
    }

    protected function content($cont){
        switch($cont->content_type){
            case "image":
                return "<img src=".$cont->content." alt=\"no data\" style=\"width:50%\"><br>";
                break;
            case "title":
                return "<h2>".$cont->content."</h2>";
                break;
            case "text":
                return "<p style=\"text-align:left;margin-bottom: 10px; line-height: 1.75em;\">".$cont->content."</p>";
                break;
            default:
            return $cont->content;
        }
    }
}
