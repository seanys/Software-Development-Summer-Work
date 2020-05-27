<?php
defined('BASEPATH') or exit('No direct script access allowed');
// 指定允许其他域名访问  
header('Access-Control-Allow-Origin:*');  
// 响应类型  
header('Access-Control-Allow-Methods:*');  
use QCloud_WeApp_SDK\Mysql\Mysql as DB;//数据库连接，按照config中链接

class Articlelist extends CI_Controller
{
    //主函数部分
    public function index()
    {
        $count=20;//默认加载条数
        $arr=array();
        $host = 'rm-bp14fgqt2783fvljh0o.mysql.rds.aliyuncs.com:3306';
        $user = 'mc';
        $db   = 'cauth';
        $pass = 'Westbrook0';
        $sql="SELECT *
        from article_cover";
        if(isset($_GET['place'])){
            $sql=$sql." where place = '".$_GET['place']." ' ";
            $count=0;
        }
        //echo $sql;
        $conn = mysqli_connect($host, $user, $pass, $db);
        if(!$conn){
            die("连接失败: " . mysqli_connect_error());
        }
        $result = mysqli_query($conn, $sql);
        if(!$count){
            $count=mysqli_num_rows($result)>20?20:mysqli_num_rows($result);
        }
        //echo $count;
            for($i=0;$i<$count;$i++){
                $record=mysqli_fetch_assoc($result);
                $arr[]=$record;
                //echo json_encode($record);
            }
        echo json_encode($arr);
    }
}
