<?php
defined('BASEPATH') or exit('No direct script access allowed');
// 指定允许其他域名访问  
header('Access-Control-Allow-Origin:*');  
// 响应类型  
header('Access-Control-Allow-Methods:*');  
// 响应头设置  
//header('Access-Control-Allow-Headers:x-POSTed-with,content-type');   
use QCloud_WeApp_SDK\Mysql\Mysql as DB;//数据库连接，按照config中链接

class Register extends CI_Controller
{
    //主函数部分
    public function index()
    {
        $check=DB::row('users',['*'], [
            'user_id' => $_POST['user_id']
        ]);
        if($check){
            echo "Account already exists";
        }
        else{
        $res=DB::insert('users', [
            'user_id' => $_POST['user_id'],
            'nickname' => $_POST['nickname'],
            'password' => $_POST['password'],
            'imageurl' => $_POST['imageurl']
        ]);
        if($res>0){
        echo "success";
        }
    }
        
    }
}
