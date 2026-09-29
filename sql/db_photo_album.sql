/*
SQLyog Community v13.2.0 (64 bit)
MySQL - 8.1.0 : Database - db_photo_album
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`db_photo_album` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `db_photo_album`;

/*Table structure for table `t_admin` */

DROP TABLE IF EXISTS `t_admin`;

CREATE TABLE `t_admin` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `password` varchar(100) NOT NULL COMMENT '密码',
  `nickname` varchar(50) DEFAULT NULL COMMENT '昵称',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机号',
  `email` varchar(100) DEFAULT NULL COMMENT '邮箱',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='管理员表';

/*Data for the table `t_admin` */

insert  into `t_admin`(`id`,`username`,`password`,`nickname`,`avatar`,`phone`,`email`,`create_time`) values 
(1,'python222','123456','系统管理员','/uploads31/photo/51673d5801dc4e8da3a6ce46e0858392.jpg','13800000001','admin@photo.com','2026-08-01 09:00:00'),
(2,'manager','123456','相册管理员','/uploads31/avatar/manager.jpg','13800000002','manager@photo.com','2026-08-02 10:00:00');

/*Table structure for table `t_album` */

DROP TABLE IF EXISTS `t_album`;

CREATE TABLE `t_album` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `category_id` bigint DEFAULT NULL COMMENT '分类ID',
  `name` varchar(100) NOT NULL COMMENT '相册名称',
  `cover` varchar(255) DEFAULT NULL COMMENT '封面图',
  `description` varchar(500) DEFAULT NULL COMMENT '描述',
  `is_public` tinyint DEFAULT '1' COMMENT '是否公开:1公开 0私密',
  `photo_count` int DEFAULT '0' COMMENT '照片数量',
  `view_count` int DEFAULT '0' COMMENT '浏览次数',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_category_id` (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='相册表';

/*Data for the table `t_album` */

insert  into `t_album`(`id`,`user_id`,`category_id`,`name`,`cover`,`description`,`is_public`,`photo_count`,`view_count`,`create_time`) values 
(2,1,3,'云南之旅','/uploads31/photo/08c1f81fec69443bbc7e8532f719a77e.png','2026年云南旅行相册',1,4,256,'2026-08-03 10:00:00'),
(4,2,4,'美食探店','/uploads31/photo/3eea51f8edb44be7a17e31c262fb3a9a.png','城市美食打卡',1,4,167,'2026-08-05 12:00:00'),
(5,3,5,'萌宠日常','/uploads31/photo/cb6e57768b164284974024bc0d3570d3.png','我家猫咪的日常',1,3,203,'2026-08-06 13:00:00'),
(6,3,6,'生活碎片','/uploads31/photo/c5734b4429d3464b8ede15822da3d916.png','记录平凡生活',0,3,45,'2026-08-07 14:00:00'),
(7,4,1,'城市夜景','/uploads31/photo/14a15c39cd5e47f782feeaae30f53de4.png','城市灯光夜景',1,3,312,'2026-08-02 15:00:00'),
(8,4,3,'西藏之行','/uploads31/photo/e002c633dab8434f92635b6cf903c07e.png','西藏自驾游',1,3,178,'2026-08-03 16:00:00'),
(10,5,6,'周末随拍','/uploads31/photo/63a2058914b14f6fa34db21ca74d9195.png','周末随手拍',0,2,56,'2026-08-05 18:00:00'),
(11,6,4,'烘焙日记','/uploads31/photo/0767e284f50346b89db21d26458e1683.png','自制烘焙作品',1,3,134,'2026-08-06 19:00:00'),
(12,6,5,'狗狗乐园','/uploads31/photo/06af1ca24eca45abb028a2c97af4ba85.png','金毛犬日常',1,3,98,'2026-08-07 20:00:00'),
(14,7,3,'旅行随拍','/uploads31/photo/e64d35d3c12543a08fc148335ed113be.png','旅行随拍，记录下',1,3,0,'2026-08-08 09:21:14');

/*Table structure for table `t_category` */

DROP TABLE IF EXISTS `t_category`;

CREATE TABLE `t_category` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(50) NOT NULL COMMENT '分类名称',
  `sort_num` int DEFAULT '0' COMMENT '排序号',
  `remark` varchar(255) DEFAULT NULL COMMENT '备注',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='相册分类表';

/*Data for the table `t_category` */

insert  into `t_category`(`id`,`name`,`sort_num`,`remark`,`create_time`) values 
(1,'风景',1,'自然风光类相册','2026-08-01 08:00:00'),
(2,'人物',2,'人物肖像类相册','2026-08-01 08:10:00'),
(3,'旅行',3,'旅行记录类相册','2026-08-01 08:20:00'),
(4,'美食',4,'美食摄影类相册','2026-08-01 08:30:00'),
(5,'宠物',5,'宠物萌照类相册','2026-08-01 08:40:00'),
(6,'生活',6,'日常生活类相册','2026-08-01 08:50:00');

/*Table structure for table `t_comment` */

DROP TABLE IF EXISTS `t_comment`;

CREATE TABLE `t_comment` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `photo_id` bigint NOT NULL COMMENT '照片ID',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `content` varchar(500) NOT NULL COMMENT '评论内容',
  `status` tinyint DEFAULT '0' COMMENT '状态:0待审核 1通过 2驳回',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_photo_id` (`photo_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='评论表';

/*Data for the table `t_comment` */

insert  into `t_comment`(`id`,`photo_id`,`user_id`,`content`,`status`,`create_time`) values 
(9,45,2,'非常不错',2,'2026-08-08 08:53:43'),
(10,71,7,'不错',1,'2026-08-08 09:59:25'),
(11,65,7,'看起来不错啊',1,'2026-08-08 09:59:47'),
(12,71,1,'不错啊',1,'2026-08-08 10:00:50'),
(13,43,1,'不错啊',1,'2026-08-08 10:05:30'),
(14,71,1,'可以的',1,'2026-08-08 10:08:55'),
(15,62,3,'不错啊',0,'2026-08-09 09:34:09'),
(16,71,3,'可以的，哈哈',0,'2026-08-09 09:34:23');

/*Table structure for table `t_favorite` */

DROP TABLE IF EXISTS `t_favorite`;

CREATE TABLE `t_favorite` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `photo_id` bigint NOT NULL COMMENT '照片ID',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_photo_user` (`photo_id`,`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='收藏表';

/*Data for the table `t_favorite` */

insert  into `t_favorite`(`id`,`photo_id`,`user_id`,`create_time`) values 
(7,69,7,'2026-08-08 09:59:36'),
(8,63,7,'2026-08-08 09:59:54'),
(9,66,7,'2026-08-08 09:59:57'),
(10,71,1,'2026-08-08 10:00:47'),
(11,66,1,'2026-08-08 10:01:06'),
(12,68,1,'2026-08-08 10:01:07'),
(13,71,3,'2026-08-08 10:11:08'),
(14,70,3,'2026-08-08 10:11:09'),
(15,69,3,'2026-08-08 10:11:10'),
(16,64,3,'2026-08-08 10:11:15'),
(17,51,3,'2026-08-08 10:56:27'),
(18,62,3,'2026-08-09 09:34:03');

/*Table structure for table `t_like` */

DROP TABLE IF EXISTS `t_like`;

CREATE TABLE `t_like` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `photo_id` bigint NOT NULL COMMENT '照片ID',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_photo_user` (`photo_id`,`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='点赞表';

/*Data for the table `t_like` */

insert  into `t_like`(`id`,`photo_id`,`user_id`,`create_time`) values 
(11,40,1,'2026-08-08 08:43:11'),
(12,45,2,'2026-08-08 08:53:37'),
(13,71,7,'2026-08-08 09:59:20'),
(14,65,7,'2026-08-08 09:59:42'),
(15,66,7,'2026-08-08 09:59:58'),
(16,71,1,'2026-08-08 10:00:47'),
(17,43,1,'2026-08-08 10:05:24'),
(18,71,3,'2026-08-08 10:11:09'),
(19,64,3,'2026-08-08 10:11:14'),
(20,51,3,'2026-08-08 10:56:26'),
(21,62,3,'2026-08-09 09:34:02');

/*Table structure for table `t_log` */

DROP TABLE IF EXISTS `t_log`;

CREATE TABLE `t_log` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `user_type` varchar(20) DEFAULT NULL COMMENT '用户类型:ADMIN/USER',
  `user_id` bigint DEFAULT NULL COMMENT '用户ID',
  `username` varchar(50) DEFAULT NULL COMMENT '用户名',
  `operation` varchar(200) DEFAULT NULL COMMENT '操作描述',
  `ip` varchar(50) DEFAULT NULL COMMENT 'IP地址',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=147 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='操作日志表';

/*Data for the table `t_log` */

insert  into `t_log`(`id`,`user_type`,`user_id`,`username`,`operation`,`ip`,`create_time`) values 
(1,'ADMIN',1,'admin','管理员登录系统','127.0.0.1','2026-08-07 08:00:00'),
(2,'USER',1,'zhangsan','用户登录系统','127.0.0.1','2026-08-07 09:00:00'),
(3,'USER',1,'zhangsan','上传照片','127.0.0.1','2026-08-07 09:30:00'),
(4,'USER',2,'lisi','创建相册','127.0.0.1','2026-08-07 10:00:00'),
(5,'ADMIN',1,'admin','审核评论','127.0.0.1','2026-08-07 11:00:00'),
(6,'USER',3,'wangwu','点赞照片','127.0.0.1','2026-08-07 12:00:00'),
(7,'USER',4,'zhaoliu','收藏照片','127.0.0.1','2026-08-07 13:00:00'),
(8,'ADMIN',2,'manager','发布公告','127.0.0.1','2026-08-07 14:00:00'),
(9,'USER',1,'zhangsan','上传照片','127.0.0.1','2026-08-08 08:31:22'),
(10,'USER',1,'zhangsan','修改相册','127.0.0.1','2026-08-08 08:39:59'),
(11,'USER',1,'zhangsan','删除照片','127.0.0.1','2026-08-08 08:42:37'),
(12,'USER',1,'zhangsan','点赞照片','127.0.0.1','2026-08-08 08:43:11'),
(13,'USER',1,'zhangsan','上传照片','127.0.0.1','2026-08-08 08:44:30'),
(14,'USER',1,'zhangsan','删除照片','127.0.0.1','2026-08-08 08:44:38'),
(15,'USER',1,'zhangsan','删除照片','127.0.0.1','2026-08-08 08:45:22'),
(16,'USER',1,'zhangsan','删除照片','127.0.0.1','2026-08-08 08:45:26'),
(17,'USER',1,'zhangsan','上传照片','127.0.0.1','2026-08-08 08:45:43'),
(18,'USER',1,'zhangsan','上传照片','127.0.0.1','2026-08-08 08:46:09'),
(19,'USER',1,'zhangsan','创建相册','127.0.0.1','2026-08-08 08:46:47'),
(20,'USER',1,'zhangsan','上传照片','127.0.0.1','2026-08-08 08:47:03'),
(21,'USER',1,'zhangsan','修改相册','127.0.0.1','2026-08-08 08:47:12'),
(22,'USER',1,'zhangsan','删除照片','127.0.0.1','2026-08-08 08:47:17'),
(23,'USER',1,'zhangsan','删除相册','127.0.0.1','2026-08-08 08:47:22'),
(24,'USER',2,'lisi','修改相册','127.0.0.1','2026-08-08 08:50:25'),
(25,'USER',2,'lisi','删除照片','127.0.0.1','2026-08-08 08:50:32'),
(26,'USER',2,'lisi','上传照片','127.0.0.1','2026-08-08 08:50:37'),
(27,'USER',2,'lisi','删除照片','127.0.0.1','2026-08-08 08:51:30'),
(28,'USER',2,'lisi','上传照片','127.0.0.1','2026-08-08 08:52:02'),
(29,'USER',2,'lisi','删除照片','127.0.0.1','2026-08-08 08:52:12'),
(30,'USER',2,'lisi','上传照片','127.0.0.1','2026-08-08 08:52:50'),
(31,'USER',2,'lisi','删除照片','127.0.0.1','2026-08-08 08:53:06'),
(32,'USER',2,'lisi','上传照片','127.0.0.1','2026-08-08 08:53:30'),
(33,'USER',2,'lisi','点赞照片','127.0.0.1','2026-08-08 08:53:37'),
(34,'USER',2,'lisi','发表评论','127.0.0.1','2026-08-08 08:53:43'),
(35,'USER',2,'lisi','删除照片','127.0.0.1','2026-08-08 08:55:13'),
(36,'USER',2,'lisi','删除照片','127.0.0.1','2026-08-08 08:55:16'),
(37,'USER',2,'lisi','删除照片','127.0.0.1','2026-08-08 08:55:19'),
(38,'USER',2,'lisi','删除相册','127.0.0.1','2026-08-08 08:55:24'),
(39,'USER',3,'wangwu','修改相册','127.0.0.1','2026-08-08 08:56:44'),
(40,'USER',3,'wangwu','删除照片','127.0.0.1','2026-08-08 08:56:52'),
(41,'USER',3,'wangwu','删除照片','127.0.0.1','2026-08-08 08:56:55'),
(42,'USER',3,'wangwu','删除照片','127.0.0.1','2026-08-08 08:56:57'),
(43,'USER',3,'wangwu','上传照片','127.0.0.1','2026-08-08 08:57:05'),
(44,'USER',3,'wangwu','上传照片','127.0.0.1','2026-08-08 08:57:22'),
(45,'USER',3,'wangwu','上传照片','127.0.0.1','2026-08-08 08:57:32'),
(46,'USER',4,'zhaoliu','删除照片','127.0.0.1','2026-08-08 08:59:22'),
(47,'USER',4,'zhaoliu','上传照片','127.0.0.1','2026-08-08 08:59:30'),
(48,'USER',4,'zhaoliu','删除照片','127.0.0.1','2026-08-08 09:00:07'),
(49,'USER',4,'zhaoliu','上传照片','127.0.0.1','2026-08-08 09:00:12'),
(50,'USER',4,'zhaoliu','删除照片','127.0.0.1','2026-08-08 09:00:28'),
(51,'USER',4,'zhaoliu','上传照片','127.0.0.1','2026-08-08 09:00:52'),
(52,'USER',4,'zhaoliu','修改相册','127.0.0.1','2026-08-08 09:01:23'),
(53,'USER',4,'zhaoliu','删除照片','127.0.0.1','2026-08-08 09:01:52'),
(54,'USER',4,'zhaoliu','修改相册','127.0.0.1','2026-08-08 09:02:44'),
(55,'USER',4,'zhaoliu','删除照片','127.0.0.1','2026-08-08 09:02:50'),
(56,'USER',4,'zhaoliu','删除照片','127.0.0.1','2026-08-08 09:02:52'),
(57,'USER',4,'zhaoliu','删除照片','127.0.0.1','2026-08-08 09:02:54'),
(58,'USER',4,'zhaoliu','上传照片','127.0.0.1','2026-08-08 09:03:00'),
(59,'USER',4,'zhaoliu','上传照片','127.0.0.1','2026-08-08 09:03:14'),
(60,'USER',4,'zhaoliu','上传照片','127.0.0.1','2026-08-08 09:03:23'),
(61,'USER',5,'sunqi','修改相册','127.0.0.1','2026-08-08 09:05:23'),
(62,'USER',5,'sunqi','删除照片','127.0.0.1','2026-08-08 09:05:29'),
(63,'USER',5,'sunqi','删除照片','127.0.0.1','2026-08-08 09:05:31'),
(64,'USER',5,'sunqi','上传照片','127.0.0.1','2026-08-08 09:05:38'),
(65,'USER',5,'sunqi','上传照片','127.0.0.1','2026-08-08 09:05:52'),
(66,'USER',5,'sunqi','删除照片','127.0.0.1','2026-08-08 09:07:18'),
(67,'USER',5,'sunqi','删除照片','127.0.0.1','2026-08-08 09:07:20'),
(68,'USER',5,'sunqi','删除照片','127.0.0.1','2026-08-08 09:07:22'),
(69,'USER',5,'sunqi','删除相册','127.0.0.1','2026-08-08 09:07:26'),
(70,'USER',6,'zhouba','修改相册','127.0.0.1','2026-08-08 09:07:54'),
(71,'USER',6,'zhouba','删除照片','127.0.0.1','2026-08-08 09:07:58'),
(72,'USER',6,'zhouba','删除照片','127.0.0.1','2026-08-08 09:08:00'),
(73,'USER',6,'zhouba','上传照片','127.0.0.1','2026-08-08 09:08:07'),
(74,'USER',6,'zhouba','上传照片','127.0.0.1','2026-08-08 09:08:22'),
(75,'USER',6,'zhouba','上传照片','127.0.0.1','2026-08-08 09:08:58'),
(76,'USER',6,'zhouba','删除照片','127.0.0.1','2026-08-08 09:10:43'),
(77,'USER',6,'zhouba','上传照片','127.0.0.1','2026-08-08 09:10:49'),
(78,'USER',6,'zhouba','删除照片','127.0.0.1','2026-08-08 09:11:14'),
(79,'USER',6,'zhouba','上传照片','127.0.0.1','2026-08-08 09:11:21'),
(80,'USER',6,'zhouba','删除照片','127.0.0.1','2026-08-08 09:11:28'),
(81,'USER',6,'zhouba','上传照片','127.0.0.1','2026-08-08 09:11:42'),
(82,'USER',6,'zhouba','修改相册','127.0.0.1','2026-08-08 09:11:56'),
(83,'USER',3,'wangwu','修改相册','127.0.0.1','2026-08-08 09:18:17'),
(84,'USER',3,'wangwu','删除照片','127.0.0.1','2026-08-08 09:18:28'),
(85,'USER',3,'wangwu','删除照片','127.0.0.1','2026-08-08 09:18:29'),
(86,'USER',3,'wangwu','删除照片','127.0.0.1','2026-08-08 09:18:32'),
(87,'USER',3,'wangwu','上传照片','127.0.0.1','2026-08-08 09:18:36'),
(88,'USER',3,'wangwu','上传照片','127.0.0.1','2026-08-08 09:18:47'),
(89,'USER',3,'wangwu','上传照片','127.0.0.1','2026-08-08 09:19:00'),
(90,'USER',7,'lili','创建相册','127.0.0.1','2026-08-08 09:21:14'),
(91,'USER',7,'lili','上传照片','127.0.0.1','2026-08-08 09:21:23'),
(92,'USER',7,'lili','上传照片','127.0.0.1','2026-08-08 09:21:35'),
(93,'USER',7,'lili','上传照片','127.0.0.1','2026-08-08 09:21:44'),
(94,'USER',7,'lili','点赞照片','127.0.0.1','2026-08-08 09:59:20'),
(95,'USER',7,'lili','发表评论','127.0.0.1','2026-08-08 09:59:25'),
(96,'USER',7,'lili','收藏照片','127.0.0.1','2026-08-08 09:59:36'),
(97,'USER',7,'lili','点赞照片','127.0.0.1','2026-08-08 09:59:42'),
(98,'USER',7,'lili','发表评论','127.0.0.1','2026-08-08 09:59:47'),
(99,'USER',7,'lili','收藏照片','127.0.0.1','2026-08-08 09:59:54'),
(100,'USER',7,'lili','收藏照片','127.0.0.1','2026-08-08 09:59:57'),
(101,'USER',7,'lili','点赞照片','127.0.0.1','2026-08-08 09:59:58'),
(102,'USER',1,'zhangsan','点赞照片','127.0.0.1','2026-08-08 10:00:47'),
(103,'USER',1,'zhangsan','收藏照片','127.0.0.1','2026-08-08 10:00:47'),
(104,'USER',1,'zhangsan','发表评论','127.0.0.1','2026-08-08 10:00:50'),
(105,'USER',1,'zhangsan','收藏照片','127.0.0.1','2026-08-08 10:01:06'),
(106,'USER',1,'zhangsan','收藏照片','127.0.0.1','2026-08-08 10:01:07'),
(107,'ADMIN',1,'java1234','删除照片','127.0.0.1','2026-08-08 10:02:09'),
(108,'ADMIN',1,'java1234','删除照片','127.0.0.1','2026-08-08 10:02:12'),
(109,'ADMIN',1,'java1234','删除照片','127.0.0.1','2026-08-08 10:02:14'),
(110,'ADMIN',1,'java1234','删除照片','127.0.0.1','2026-08-08 10:02:16'),
(111,'ADMIN',1,'java1234','删除照片','127.0.0.1','2026-08-08 10:02:18'),
(112,'ADMIN',1,'java1234','审核评论','127.0.0.1','2026-08-08 10:02:23'),
(113,'ADMIN',1,'java1234','审核评论','127.0.0.1','2026-08-08 10:02:24'),
(114,'ADMIN',1,'java1234','审核评论','127.0.0.1','2026-08-08 10:02:24'),
(115,'ADMIN',1,'java1234','审核评论','127.0.0.1','2026-08-08 10:02:27'),
(116,'USER',1,'zhangsan','点赞照片','127.0.0.1','2026-08-08 10:05:24'),
(117,'USER',1,'zhangsan','发表评论','127.0.0.1','2026-08-08 10:05:30'),
(118,'ADMIN',1,'java1234','审核评论','127.0.0.1','2026-08-08 10:05:48'),
(119,'USER',1,'zhangsan','发表评论','127.0.0.1','2026-08-08 10:08:55'),
(120,'ADMIN',1,'java1234','审核评论','127.0.0.1','2026-08-08 10:09:19'),
(121,'USER',3,'wangwu','收藏照片','127.0.0.1','2026-08-08 10:11:08'),
(122,'USER',3,'wangwu','点赞照片','127.0.0.1','2026-08-08 10:11:09'),
(123,'USER',3,'wangwu','收藏照片','127.0.0.1','2026-08-08 10:11:09'),
(124,'USER',3,'wangwu','收藏照片','127.0.0.1','2026-08-08 10:11:10'),
(125,'USER',3,'wangwu','点赞照片','127.0.0.1','2026-08-08 10:11:14'),
(126,'USER',3,'wangwu','收藏照片','127.0.0.1','2026-08-08 10:11:15'),
(127,'USER',3,'wangwu','点赞照片','127.0.0.1','2026-08-08 10:56:26'),
(128,'USER',3,'wangwu','收藏照片','127.0.0.1','2026-08-08 10:56:27'),
(129,'ADMIN',1,'python222','新增用户','127.0.0.1','2026-08-09 09:31:33'),
(130,'ADMIN',1,'python222','修改用户','127.0.0.1','2026-08-09 09:31:37'),
(131,'ADMIN',1,'python222','删除用户','127.0.0.1','2026-08-09 09:31:40'),
(132,'USER',3,'wangwu','点赞照片','127.0.0.1','2026-08-09 09:34:02'),
(133,'USER',3,'wangwu','收藏照片','127.0.0.1','2026-08-09 09:34:03'),
(134,'USER',3,'wangwu','发表评论','127.0.0.1','2026-08-09 09:34:09'),
(135,'USER',3,'wangwu','发表评论','127.0.0.1','2026-08-09 09:34:23'),
(136,'USER',3,'wangwu','创建相册','127.0.0.1','2026-08-09 09:36:32'),
(137,'USER',3,'wangwu','修改相册','127.0.0.1','2026-08-09 09:36:41'),
(138,'USER',3,'wangwu','上传照片','127.0.0.1','2026-08-09 09:36:48'),
(139,'USER',3,'wangwu','收藏照片','127.0.0.1','2026-08-09 09:36:58'),
(140,'USER',3,'wangwu','创建相册','127.0.0.1','2026-08-09 09:37:11'),
(141,'USER',3,'wangwu','上传照片','127.0.0.1','2026-08-09 09:37:18'),
(142,'USER',3,'wangwu','删除照片','127.0.0.1','2026-08-09 09:37:39'),
(143,'USER',3,'wangwu','删除相册','127.0.0.1','2026-08-09 09:37:45'),
(144,'ADMIN',1,'python222','删除照片','127.0.0.1','2026-08-09 09:38:24'),
(145,'ADMIN',1,'python222','删除相册','127.0.0.1','2026-08-09 09:38:30'),
(146,'ADMIN',1,'python222','发布公告','127.0.0.1','2026-08-09 09:39:34');

/*Table structure for table `t_notice` */

DROP TABLE IF EXISTS `t_notice`;

CREATE TABLE `t_notice` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `title` varchar(200) NOT NULL COMMENT '标题',
  `content` text COMMENT '内容',
  `admin_id` bigint DEFAULT NULL COMMENT '发布管理员ID',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='公告表';

/*Data for the table `t_notice` */

insert  into `t_notice`(`id`,`title`,`content`,`admin_id`,`create_time`) values 
(1,'欢迎使用电子相册管理系统','本系统支持相册创建、照片上传、点赞收藏、评论互动等功能，祝您使用愉快！',1,'2026-08-01 09:00:00'),
(2,'系统维护通知','系统将于2026-08-10 02:00-04:00进行例行维护，届时可能短暂无法访问，请提前保存数据。',1,'2026-08-05 10:00:00'),
(3,'相册广场上线','公开相册广场已上线，欢迎浏览其他用户分享的精彩相册！',2,'2026-08-07 11:00:00');

/*Table structure for table `t_photo` */

DROP TABLE IF EXISTS `t_photo`;

CREATE TABLE `t_photo` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `album_id` bigint NOT NULL COMMENT '相册ID',
  `user_id` bigint NOT NULL COMMENT '用户ID',
  `name` varchar(100) DEFAULT NULL COMMENT '照片名称',
  `url` varchar(255) NOT NULL COMMENT '照片地址',
  `description` varchar(500) DEFAULT NULL COMMENT '描述',
  `file_size` bigint DEFAULT '0' COMMENT '文件大小(字节)',
  `view_count` int DEFAULT '0' COMMENT '浏览次数',
  `like_count` int DEFAULT '0' COMMENT '点赞数',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_album_id` (`album_id`),
  KEY `idx_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=74 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='照片表';

/*Data for the table `t_photo` */

insert  into `t_photo`(`id`,`album_id`,`user_id`,`name`,`url`,`description`,`file_size`,`view_count`,`like_count`,`create_time`) values 
(40,2,1,'梯田','/uploads31/photo/bf3c4ff3529343fbb186048e7979274e.png',NULL,5002724,0,1,'2026-08-08 08:31:22'),
(41,2,1,'雪山','/uploads31/photo/0575ae1baadc4c6b9583cb66fdbc3275.png',NULL,5441323,0,0,'2026-08-07 08:44:30'),
(42,2,1,'古城','/uploads31/photo/48c75c3bef3043d0822d735713d6efc6.png',NULL,5123961,0,0,'2026-08-08 08:45:43'),
(43,2,1,'洱海','/uploads31/photo/b9ee2285e46d482899367a04b49ad272.png',NULL,4011907,0,1,'2026-08-08 08:46:09'),
(45,4,2,'咖啡','/uploads31/photo/ae5d0a348b2e4c788064d2bb23057f6d.png',NULL,3400112,0,1,'2026-08-08 08:50:37'),
(46,4,2,'甜品','/uploads31/photo/cc75d9ac41ef493ebe8b674cce821c79.png',NULL,3762548,0,0,'2026-08-08 08:52:02'),
(47,4,2,'寿司','/uploads31/photo/a37e9f936a3e4262ae007b3036a7b6de.png',NULL,3987456,0,0,'2026-08-08 08:52:50'),
(48,4,2,'火锅','/uploads31/photo/021545e51d3c4bed98c98c10aae2dc04.png',NULL,4346294,0,0,'2026-08-08 08:53:30'),
(49,6,3,'生活碎片1','/uploads31/photo/654768cc788d4d92b876b5be6d6b8ec2.png',NULL,5416635,0,0,'2026-08-06 08:57:05'),
(50,6,3,'生活碎片2','/uploads31/photo/5ed41fd3d7f34b7485eb48f13a0d9769.png',NULL,3478887,0,0,'2026-08-07 08:57:22'),
(51,6,3,'生活碎片3','/uploads31/photo/630cdd0e2b9c4edeaa5e3f55f909d99b.png',NULL,3286149,0,1,'2026-08-08 08:57:32'),
(52,8,4,'羊湖','/uploads31/photo/d6a26f469c18429bb33efd69fa58a042.png',NULL,5910763,0,0,'2026-08-08 08:59:30'),
(53,8,4,'纳木错','/uploads31/photo/a9b5690d4afa484cab73056964f61bab.png',NULL,5762777,0,0,'2026-08-08 09:00:12'),
(54,8,4,'布达拉宫','/uploads31/photo/880f2781e04145f78e3be6f187e6a5f8.png',NULL,5072922,0,0,'2026-08-08 09:00:52'),
(55,7,4,'夜景1','/uploads31/photo/cd8fb8501bd34c34af78af68bbb3b5c5.png',NULL,5525657,0,0,'2026-08-08 09:03:00'),
(56,7,4,'夜景2','/uploads31/photo/e10247d5a1e946a5a8e019bf8f2cb0af.png',NULL,4740710,0,0,'2026-08-08 09:03:14'),
(57,7,4,'夜景3','/uploads31/photo/ed1ca6b22168486bb3d9f3370fbecb10.png',NULL,4007009,0,0,'2026-08-08 09:03:23'),
(58,10,5,'随拍1','/uploads31/photo/d00664782f1c4139b0f0fbda4704d09a.png',NULL,4577123,0,0,'2026-08-08 09:05:38'),
(59,10,5,'随拍2','/uploads31/photo/cd8f18b15fde47cbbb876e788f56d4c3.png',NULL,4943990,0,0,'2026-08-08 09:05:52'),
(60,12,6,'金毛1','/uploads31/photo/c6161285e7094a25865a7e3901ef15a2.png',NULL,4456318,0,0,'2026-08-08 09:08:07'),
(61,12,6,'金毛2','/uploads31/photo/0657ca028ce9401d9932edc7384586a5.png',NULL,3370555,0,0,'2026-08-08 09:08:22'),
(62,12,6,'金毛3','/uploads31/photo/319233ac23724a68a1fc3d5470f67f2a.png',NULL,3840754,0,1,'2026-08-08 09:08:58'),
(63,11,6,'曲奇','/uploads31/photo/178b5a8b91e64b78b7b909c69b4df839.png',NULL,3506320,0,0,'2026-08-08 09:10:49'),
(64,11,6,'面包','/uploads31/photo/a1891c12a3b641a38ee958b98fe07409.png',NULL,4031360,0,1,'2026-08-08 09:11:21'),
(65,11,6,'蛋糕','/uploads31/photo/43525aa84cf34562b1a526c15ec8293d.png',NULL,3180170,0,1,'2026-08-08 09:11:42'),
(66,5,3,'猫咪1','/uploads31/photo/667b17003e744b9f86264fe5ac9dbf00.png',NULL,3122968,0,1,'2026-08-08 09:18:36'),
(67,5,3,'猫咪2','/uploads31/photo/a323ad3e656b453d95aedd11b5099d80.png',NULL,4550867,0,0,'2026-08-07 09:18:47'),
(68,5,3,'猫咪3','/uploads31/photo/9dc74ac1b14a4192bab7a4751ed56059.png',NULL,3992045,0,0,'2026-08-08 09:19:00'),
(69,14,7,'旅行随拍1','/uploads31/photo/360432c9a14249ababd639878c18a707.png',NULL,5686470,0,0,'2026-08-08 09:21:23'),
(70,14,7,'旅行随拍2','/uploads31/photo/e0782f633b1046cbab72515422d81d31.png',NULL,5985362,0,0,'2026-08-08 09:21:35'),
(71,14,7,'旅行随拍3','/uploads31/photo/176f7e0af4714b3ba6547df19f38cc63.png',NULL,3582067,0,3,'2026-08-08 09:21:44');

/*Table structure for table `t_user` */

DROP TABLE IF EXISTS `t_user`;

CREATE TABLE `t_user` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `password` varchar(100) NOT NULL COMMENT '密码',
  `nickname` varchar(50) DEFAULT NULL COMMENT '昵称',
  `avatar` varchar(255) DEFAULT NULL COMMENT '头像',
  `gender` tinyint DEFAULT '1' COMMENT '性别:1男 2女',
  `phone` varchar(20) DEFAULT NULL COMMENT '手机号',
  `email` varchar(100) DEFAULT NULL COMMENT '邮箱',
  `status` tinyint DEFAULT '1' COMMENT '状态:1正常 0禁用',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户表';

/*Data for the table `t_user` */

insert  into `t_user`(`id`,`username`,`password`,`nickname`,`avatar`,`gender`,`phone`,`email`,`status`,`create_time`) values 
(1,'zhangsan','123456','张三','/uploads31/avatar/c2e00fc1edf94bb58351a07f92ec2414.jpg',1,'13900000002','zhangsan2@qq.com',1,'2026-08-01 10:00:00'),
(2,'lisi','123456','李四','/uploads31/avatar/74aee90599f44f0da16e48a0bb482941.jpg',1,'13900000002','lisi@qq.com',1,'2026-08-02 11:00:00'),
(3,'wangwu','123456','王五','/uploads31/avatar/a69e9a5768204004a1d0266cd7af0543.jpg',2,'13900000003','wangwu@qq.com',1,'2026-08-03 12:00:00'),
(4,'zhaoliu','123456','赵六','/uploads31/avatar/a6c77cd1dfcb44909e49ffc30562ce8d.jpg',1,'13900000004','zhaoliu@qq.com',1,'2026-08-04 13:00:00'),
(5,'sunqi','123456','孙七','/uploads31/avatar/df581ef9c91a474cb76e0f7f02c68701.jpg',2,'13900000005','sunqi@qq.com',1,'2026-08-05 14:00:00'),
(6,'zhouba','123456','周八','/uploads31/avatar/8726917756434c778a18e713d36cefd7.jpg',1,'13900000006','zhouba@qq.com',1,'2026-08-06 15:00:00'),
(7,'lili','123456','丽丽','/uploads31/avatar/8ebf9127a1d342279ce04b9ce53f3ec8.jpg',2,'18876787102',NULL,1,'2026-08-08 08:20:47');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
