/*
Copyright (C) 2012 Hema Koppula
*/

#ifndef FEATURE_GENERATION_PCL_SRC_FRAME_H_
#define FEATURE_GENERATION_PCL_SRC_FRAME_H_

#include <opencv2/opencv.hpp>
#include <pcl/point_types.h>
#include <pcl/io/pcd_io.h>
#include <assert.h>
#include <iostream>
#include <string>
#include <map>
#include <vector>

#include "./frame_skel.h"
#include "includes/color.cpp"
#include "includes/point_types.h"
#include "includes/CombineUtils.h"
#include "HOG.cpp"

typedef pcl::PointXYZRGB PointT;


#define sqr(x) ((x)*(x))

using namespace std;

class ObjectProfile {
 private:
  vector<float> eigenValues;  // sorted in ascending order

 public:
  vector<double> features;
  pcl::PointCloud<PointT> cloud;
  HOGFeaturesOfBlock avgHOGFeatsOfObject;
  float avgH;
  float avgS;
  float avgV;
  int minX, minY, maxX, maxY;
  int objID;
  vector<int> pcInds;
  string transformfile;
  string objectType;
  pcl::PointXYZ centroid;
  pcl::PointXYZ center;
  Eigen::Vector3d normal;

  ObjectProfile(vector<double> &feats, pcl::PointCloud<PointT> &fullCloud,
                map<int, int> &tablePoints, int id, string transFile);

  ObjectProfile(vector<double> &feats, pcl::PointCloud<PointT> &fullCloud,
                map<int, int> &tablePoints, int id);

  ObjectProfile(vector<double> &feats, pcl::PointCloud<PointT> &fullCloud,
                map<int, int> &tablePoints, int id, string transFile,
                vector<int> &PCInds);

  void initialize();

  void setObjectType(string);

  string getObjectType();

  void getObjectPointCloud(pcl::PointCloud<PointT> &fullCloud,
                           vector<int> &PCInds);

  void getObjectPointCloud(pcl::PointCloud<PointT> &fullCloud,
                           map<int, int> &tablePoints);

  void filterCloud(map<int, int> &tablePoints);

  void setEigValues(Eigen::Vector3d eigenValues_);

  float getDescendingLambda(int index);

  void computeCentroid();

  double getMinDistanceTo(pcl::PointXYZ p);

  double getDistanceToCentroid(pcl::PointXYZ p);

  pcl::PointXYZ getCentroid();

  void setCentroid(pcl::PointXYZ);

  void computeCenter();

  pcl::PointXYZ getCenter();

  float getScatter();

  float getLinearNess();

  float getPlanarNess();

  float getNormalZComponent();

  float getAngleWithVerticalInRadians();

  float getHorzDistanceBwCentroids(ObjectProfile & other);

  float getDistanceSqrBwCentroids(ObjectProfile & other);

  float getDistanceSqrBwCenters(const ObjectProfile & other);

  float getVertDispCentroids(const ObjectProfile & other);

  float getXDispCentroids(const ObjectProfile & other);

  float getYDispCentroids(const ObjectProfile & other);

  float getVertDispCenters(const ObjectProfile & other);

  float getHDiffAbs(const ObjectProfile & other);

  float getSDiff(const ObjectProfile & other);

  float getVDiff(const ObjectProfile & other);

  float getAngleDiffInRadians(const ObjectProfile & other);

  float getNormalDotProduct(const ObjectProfile & other);

  float getInnerness(const ObjectProfile & other);

  float pushHogDiffFeats(const ObjectProfile & other, vector<float> & feats);

  float getCoplanarity(const ObjectProfile & other);

  void printFeatures();

  void setFeatures(vector<double> &feat);
};

class Frame {
 private:
  vector<vector<double> > objFeats;
  HOG hog;
  std::vector<HOGFeaturesOfBlock> aggHogVec;
  static const int BLOCK_SIDE = 8;
  map<int, int> tablePoints;
  bool findTable;

  void createPointCloud(int ***IMAGE, string transformfile);

  void createPointCloud(int ***IMAGE);

  /* This function takes a HOG object and aggregates the HOG
     features for each stripe in the chunk.
     It populates aggHogVec with one HOGFeaturesOfBlock
     object for each stripe in the image. */
  void computeAggHogBlock(int numStripes, int minXBlock, int maxXBlock,
                          int minYBlock, int maxYBlock,
                          HOGFeaturesOfBlock &hogObject);

  void computeObjectHog();

  void computeHogDescriptors();

 public:
  static int FrameNum;
  int frameNum;
  string sequenceId;
  vector<ObjectProfile> objects;
  FrameSkel skeleton;
  pcl::PointCloud<PointT> cloud;
  vector<double> rgbdskel_feats;

  void printHOGFeats();

  void savePointCloud();

  void saveObjImage(ObjectProfile & obj, int ***IMAGE);

  void saveImage();


  // MIRRORED means skeleton is mirrored; RGBD comes in non mirrored form
  // but mirroring should be easy for RGBD

  Frame();

  Frame(int ***IMAGE, double** data, double **pos_data,
        vector<vector<double> > &objFeats, string seqId, int fnum,
        string transformfile);

  Frame(int ***IMAGE, double** data, double **pos_data,
        vector<vector<double> > &objFeats, string seqId, int fnum);

  Frame(int ***IMAGE, double** data, double **pos_data,
        vector<vector<double> > &objFeats, string seqId, int fnum,
        string transformfile, vector<vector<int> > &objPCInds);

  Frame(int ***IMAGE, double** data, double **pos_data,
        vector<vector<double> > &objFeats, string seqId, int fnum,
        string transformfile, vector<vector<int> > &objPCInds,
        vector<string> types);

  Frame(int ***IMAGE, double** data, double **pos_data,
        vector<vector<double> > &objFeats, string seqId, int fnum,
        string transformfile, vector<vector<int> > &objPCInds, bool partial);

  ~Frame();
};

#endif  // FEATURE_GENERATION_PCL_SRC_FRAME_H_
