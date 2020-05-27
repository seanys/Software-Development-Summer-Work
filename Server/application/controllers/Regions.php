<?php
defined('BASEPATH') or exit('No direct script access allowed');
// 指定允许其他域名访问  
header('Access-Control-Allow-Origin:*');  
// 响应类型  
header('Access-Control-Allow-Methods:*');  
use QCloud_WeApp_SDK\Mysql\Mysql as DB;//数据库连接，按照config中链接

class Regions extends CI_Controller
{
    //主函数部分
    public function index()
    {
        $arr=array();
        $res=DB::select('places',['name','url','id']);
        for($i=0;$i<count($res);$i++){
            if($this->check($res[$i]->name)){
                if($res[$i]->id<=113){
                    $temp=$res[$i];
                    $temp->url='中国大陆';
                    $arr[]=$temp;
                }
                elseif ($res[$i]->id<=122) {
                    $temp=$res[$i];
                    $temp->url='港澳台地区';
                    $arr[]=$temp;
                }
                elseif ($res[$i]->id<=186) {
                    $temp=$res[$i];
                    $temp->url='亚洲';
                    $arr[]=$temp;
                }
                elseif ($res[$i]->id<=202 or $res[$i]->id==258) {
                    $temp=$res[$i];
                    $temp->url='北美洲';
                    $arr[]=$temp;
                }
                elseif ($res[$i]->id<=268) {
                    $temp=$res[$i];
                    $temp->url='欧洲';
                    $arr[]=$temp;
                }
                elseif ($res[$i]->id<=278) {
                    $temp=$res[$i];
                    $temp->url='澳洲';
                    $arr[]=$temp;
                }
                else{
                    $temp=$res[$i];
                    $temp->url='非洲';
                    $arr[]=$temp;
                }
            }
        }
        echo json_encode($arr);
    }

    protected function check($city){
        $res=DB::select('article_cover',['*'],['place'=>$city]);
        return $res;
    }
}
