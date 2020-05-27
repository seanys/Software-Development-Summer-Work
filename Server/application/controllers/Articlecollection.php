<?php
defined('BASEPATH') or exit('No direct script access allowed');
// 指定允许其他域名访问  
header('Access-Control-Allow-Origin:*');  
// 响应类型  
header('Access-Control-Allow-Methods:*');  
use QCloud_WeApp_SDK\Mysql\Mysql as DB;//数据库连接，按照config中链接

class Articlecollection extends CI_Controller
{
    //单user_id:取出用户收藏
    //user_id+article_id:用户添加收藏
    //user_id+article_id,action=1:查询用户是否收藏该文章
    //主函数部分
    public function index()
    {
        if(isset($_GET['user_id'])){
            if(isset($_GET['article_id'])){ 
                if(!isset($_GET['action'])){  //添加收藏
                    $temp=DB::insert('article_collection', [
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
                else{
                    //echo "检查收藏";
                    if($_GET['action']==1){
                        //echo "检查收藏";
                        $host = 'rm-bp14fgqt2783fvljh0o.mysql.rds.aliyuncs.com:3306';
                        $user = 'mc';
                        $db   = 'cauth';
                        $pass = 'Westbrook0';
                        $sql='SELECT * FROM article_collection where user_id = '.$_GET['user_id'].' and article_id = '.$_GET['article_id'];
                        $conn = mysqli_connect($host, $user, $pass, $db);
                        if(!$conn){
                            die("连接失败: " . mysqli_connect_error());
                        }
                        $result = mysqli_query($conn, $sql);
                        if(mysqli_num_rows($result)){
                            echo "true";//用户已收藏
                        }
                        else{
                            echo "false";//用户未收藏
                        }
                    }
                }
                }
            else{  //取出收藏
                $list= DB::select('article_collection', ['*'], " user_id ='".$_GET['user_id']."'");
                $id="(";
                if(count($list)){
                    for($i=0;$i<count($list)-1;$i++){
                        $id=$id."'".$list[$i]->article_id."',";
                    }
                    $id=$id."'".$list[$i]->article_id."') ";
                }
                $arr=array();
                $host = 'rm-bp14fgqt2783fvljh0o.mysql.rds.aliyuncs.com:3306';
                $user = 'mc';
                $db   = 'cauth';
                $pass = 'Westbrook0';
                $sql="SELECT *
                from article_cover where article_id in" .$id;
                //echo $sql;
                $conn = mysqli_connect($host, $user, $pass, $db);
                if(!$conn){
                    die("连接失败: " . mysqli_connect_error());
                }
                $result = mysqli_query($conn, $sql);
                if (!$result){
                    echo '无数据';
                    exit();
                }
                $count=mysqli_num_rows($result);
                //echo $count;
                    for($i=0;$i<$count;$i++){
                        $record=mysqli_fetch_assoc($result);
                        $arr[]=$record;
                        //echo json_encode($record);
                    }
                echo json_encode($arr);
                }
            }
        else{
            echo "no parameter";
        }
        
    }
}