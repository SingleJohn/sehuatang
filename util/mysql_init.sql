#建库
create database sehuatang default character set utf8mb4 collate utf8mb4_unicode_ci;
-- #创建用户
-- create user 'sehuatang'@'localhost' identified by 'sehuatang';
-- #设置权限
-- grant all privileges on sehuatang.* to 'sehuatang'@'%';
-- #刷新权限
-- flush privileges;
#创建表
create table sehuatang.sht_data
(
    id        int auto_increment comment 'id'
        primary key,
    magnet    varchar(150)  null comment '磁力链接',
    number    varchar(200)  null comment '番号',
    title     varchar(200) null comment '标题',
    post_time timestamp    null comment '发布时间',
    date      date    null comment '日期',
    tid       int          null comment '网站页面标识',
    fid       int          null comment '板块标识'
);
create table sehuatang.sht_images
(
    id       int auto_increment comment 'id'
        primary key,
    sht_data_id int null comment '关联数据id',
    image_url varchar(200) null comment '图片地址'
);