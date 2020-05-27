<?php
defined('BASEPATH') or exit('No direct script access allowed');
// 指定允许其他域名访问  
header('Access-Control-Allow-Origin:*');  
// 响应类型  
header('Access-Control-Allow-Methods:*');  
// 响应头设置  
//header('Access-Control-Allow-Headers:x-POSTed-with,content-type');   
use QCloud_WeApp_SDK\Mysql\Mysql as DB;//数据库连接，按照config中链接

class Login extends CI_Controller
{
    //主函数部分
    public function index()
    {
    if (isset($_POST['user_id']) and isset($_POST['password'])){
	$res=DB::select('users',['*'],"user_id=".$_POST['user_id']);
	if(count($res)>0){
	    $psw=$res[0]->password;
	    if(!strcmp($psw,$_POST['password'])){
	        echo json_encode($res[0]);  //登录信息
	    }
	    else{
	        echo "password error";  //密码错误
	    }
	}
	else{
	    echo "account not exist";  //账户不存在
        }	
    }
    }
}
