/*
 Navicat Premium Dump SQL

 Source Server         : hyyb
 Source Server Type    : SQLite
 Source Server Version : 3045000 (3.45.0)
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3045000 (3.45.0)
 File Encoding         : 65001

 Date: 19/04/2025 07:59:29
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS "admin";
CREATE TABLE "admin" (

);

-- ----------------------------
-- Table structure for attendance
-- ----------------------------
DROP TABLE IF EXISTS "attendance";
CREATE TABLE "attendance" (

);

-- ----------------------------
-- Table structure for department
-- ----------------------------
DROP TABLE IF EXISTS "department";
CREATE TABLE "department" (

);

-- ----------------------------
-- Table structure for departmentp
-- ----------------------------
DROP TABLE IF EXISTS "departmentp";
CREATE TABLE "departmentp" (

);

-- ----------------------------
-- Table structure for diary
-- ----------------------------
DROP TABLE IF EXISTS "diary";
CREATE TABLE "diary" (

);

-- ----------------------------
-- Table structure for hazard
-- ----------------------------
DROP TABLE IF EXISTS "hazard";
CREATE TABLE "hazard" (

);

-- ----------------------------
-- Table structure for jobcategory
-- ----------------------------
DROP TABLE IF EXISTS "jobcategory";
CREATE TABLE "jobcategory" (

);

-- ----------------------------
-- Table structure for link
-- ----------------------------
DROP TABLE IF EXISTS "link";
CREATE TABLE "link" (
  "id" INTEGER NOT NULL,
  "name" VARCHAR(30),
  "url" VARCHAR(255),
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Table structure for message
-- ----------------------------
DROP TABLE IF EXISTS "message";
CREATE TABLE "message" (

);

-- ----------------------------
-- Table structure for spare
-- ----------------------------
DROP TABLE IF EXISTS "spare";
CREATE TABLE "spare" (

);

-- ----------------------------
-- Table structure for stuff
-- ----------------------------
DROP TABLE IF EXISTS "stuff";
CREATE TABLE "stuff" (

);

-- ----------------------------
-- Indexes structure for table diary
-- ----------------------------
CREATE INDEX "ix_diary_datestamp"
ON "diary" (
  "datestamp" ASC
);

-- ----------------------------
-- Indexes structure for table hazard
-- ----------------------------
CREATE INDEX "ix_hazard_timestamp"
ON "hazard" (
  "timestamp" ASC
);

-- ----------------------------
-- Indexes structure for table message
-- ----------------------------
CREATE INDEX "ix_message_timestamp"
ON "message" (
  "timestamp" ASC
);

-- ----------------------------
-- Indexes structure for table spare
-- ----------------------------
CREATE INDEX "ix_spare_timestamp"
ON "spare" (
  "timestamp" ASC
);

PRAGMA foreign_keys = true;
