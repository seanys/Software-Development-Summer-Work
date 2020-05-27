<?php
defined('BASEPATH') or exit('No direct script access allowed');
// 指定允许其他域名访问  
header('Access-Control-Allow-Origin:*');  
// 响应类型  
header('Access-Control-Allow-Methods:*');  
use QCloud_WeApp_SDK\Mysql\Mysql as DB;//数据库连接，按照config中链接
date_default_timezone_set('PRC');
class Routecollection extends CI_Controller
{  //action 1=>储存 2=>删除 3=>查询
    //主函数部分
    public function index()
    {
        if(isset($_GET['action'])){  //储存数据,action=1，其余数据必须要传，可空
            if($_GET['action']=='1'){
                $temp=DB::insert('history', [
                    'user_id' => $_GET['user_id'],
                    'traffic' => $_GET['traffic'],
                    'hotel' => $_GET['hotel'],
                    'slights' => $_GET['slights'],
                    'title' => $_GET['title'],
                    'introduce' => $_GET['introduce'],
                    'time' => date('Y-m-d H:i:s')
                ]);
                    if($temp){
                        echo "succeed";
                    }
                    else{
                        echo "failed";
                    }
            }
            elseif ($_GET['action']=='2'){ //删除数据，action填入2，然后必须传id
                $temp=DB::delete('history', [
                    'id' => $_GET['id']
                ]);
                if($temp){
                    echo "delete succeed";
                }
                else{
                    echo "delete failed";
                }
            }
            elseif($_GET['action']=='3'){  //查询数据，action填入3且仅传user_id：
                $arr=array();

                $history=DB::raw("SELECT history.title,history.introduce,history.aim_city,places.normal_picture FROM history LEFT JOIN places ON places.name=history.aim_city WHERE history.user_id=".$_GET['user_id']);
                $history=$history->fetchAll();
                //$temp=DB::select('history', ['*'], ["user_id = '".$_GET['user_id']."'"]);
                if(count($history)){
                    $this->json([
                        'code' => 1,
                        'data' => [
                            "history"=> $history
                        ],
                    ]);
                }
                else{
                    $this->json([
                        'code' => 0,
                        'data' => [
                            "history"=> $history
                        ],
                    ]);
                }
            }
        }
    }
}