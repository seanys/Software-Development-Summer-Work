<?php
defined('BASEPATH') or exit('No direct script access allowed');
// 指定允许其他域名访问  
header('Access-Control-Allow-Origin:*');  
// 响应类型  
header('Access-Control-Allow-Methods:*');  
// 响应头设置  
//header('Access-Control-Allow-Headers:x-POSTed-with,content-type');   
use QCloud_WeApp_SDK\Mysql\Mysql as DB;//数据库连接，按照config中链接

class Info extends CI_Controller
{
    //主函数部分
    public function index()
    {
	$res=DB::row('users',['user_id','nickname','imageurl'],"user_id=".$_GET['user_id']);
	if(count($res)>0){
        echo json_encode($res);
	}
	else{
	    echo "account not exist";  //账户不存在
        }	
    }
}

