<?php
defined('BASEPATH') or exit('No direct script access allowed');
header('Access-Control-Allow-Origin:*');    
header('Access-Control-Allow-Methods:*');  
//header('Access-Control-Allow-Headers:x-requested-with,content-type');   
use QCloud_WeApp_SDK\Mysql\Mysql as DB;//数据库连接，按照config中链接

class Upload extends CI_Controller
{
    //主函数部分
    public function index()
    {
        $temp=DB::row('Articles', ['max(id) as id']);
        $nowId=$temp->id;
        $nowId++;
        /*$res1=DB::insert('articles', [
            'id' => null,
            'author_id' => $_POST['user_id'],
            'title' => $_POST['title'],
            'publish_time' => date('Y-m-d H:i:s'),
            'article_type' => "",
            'place' => $_POST['place'],
            'sight' => "",
            'from' => "user",
            'url' => "",
            'exist' => 1
        ]);*/
                $host = 'rm-bp14fgqt2783fvljh0o.mysql.rds.aliyuncs.com:3306';
                $user = 'mc';
                $db   = 'cauth';
                $pass = 'Westbrook0';
                $sql="insert into articles values($nowId,'$_POST[user_id]','$_POST[title]',NOW(),'','$_POST[place]','','user','',1)";
                $conn = mysqli_connect($host, $user, $pass, $db);
                if(!$conn){
                    die("连接失败: " . mysqli_connect_error());
                }
                //echo $sql;
                $result = mysqli_query($conn, $sql);
                if(!$result){
                    die("failed");
                }
        /*$res2=DB::insert('article_content', [
            'id' => null,
            'article_id' => $nowId,
            'content_type' => 'HTML',
            'content' => $_POST['content']
        ]);*/
        $sql="insert into article_content values(null,$nowId,'HTML','$_POST[content]','')";
        //echo $sql;
                $conn = mysqli_connect($host, $user, $pass, $db);
                if(!$conn){
                    die("连接失败: " . mysqli_connect_error());
                }

                $result = mysqli_query($conn, $sql);
                if(!$result){
                    die("failed");
                }
        /*$res3=DB::insert('article_cover', [
            'article_id' => $nowId,
            'title' => $_POST['title'],
            'place' => $_POST['place'],
            'image' => $_POST['image'],
            'introduce' => $_POST['introduce']
        ]);*/
        $sql="insert into article_cover values($nowId,'$_POST[title]','$_POST[place]','$_POST[image]','$_POST[introduce]')";
        //echo $sql;
        $conn = mysqli_connect($host, $user, $pass, $db);
        if(!$conn){
            die("连接失败: " . mysqli_connect_error());
        }
        $result = mysqli_query($conn, $sql);
        if(!$result){
            die("failed");
        }
        echo $nowId;
    }

}
