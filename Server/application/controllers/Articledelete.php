<?php
defined('BASEPATH') or exit('No direct script access allowed');
// 指定允许其他域名访问  
header('Access-Control-Allow-Origin:*');  
// 响应类型  
header('Access-Control-Allow-Methods:*');  
use QCloud_WeApp_SDK\Mysql\Mysql as DB;//数据库连接，按照config中链接

class Articledelete extends CI_Controller
{
    //主函数部分
    public function index()
    {
        if(isset($_GET['user_id'])){
            if(isset($_GET['article_id'])){  //添加收藏
                $temp=DB::delete('article_collection', [
                    'user_id' => $_GET['user_id'],
                    'article_id' => $_GET['article_id']
                ]);
                    if($temp){
                        echo "succeed";
                    }
                    else{
                        echo "failed";
                    }
                }
            }
        else{
            echo "no parameter";
        }
        
    }
}