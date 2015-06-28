/*
Copyright (C) 2012 Hema Koppula
*/

#ifndef FEATURE_GENERATION_PCL_SRC_FRAME_SKEL_H_
#define FEATURE_GENERATION_PCL_SRC_FRAME_SKEL_H_


#include <vector>
#include <string>

#include "includes/point_types.h"
#include "includes/CombineUtils.h"
#include "./constants.h"


typedef pcl::PointXYZRGB PointT;

class FrameSkel {
 public:
  double **data;  // [JOINT_NUM][JOINT_DATA_NUM];
  int **data_CONF;  // [JOINT_NUM][JOINT_DATA_TYPE_NUM]
  double **pos_data;  // [POS_JOINT_NUM][POS_JOINT_DATA_NUM];
  int *pos_data_CONF;  // [POS_JOINT_NUM]
  int num_local_joints;
  vector<pcl::PointXYZ> transformed_joints;
  pcl::PointXYZ headOrientation;

  double ** joints_local;
  vector<int> jointList;
  vector<int> pos_jointList;
  int frameId;

  double* computeLocalLoc(double head_ori[9], double head_pos[3],
                          double hand_pos[3]);

  void computePosition();

  void transformJointPositions(string transformFile);

  void initialize(double **data_, double **pos_data_, string transformFile);

  void initialize_partial(double **data_, double **pos_data_,
                          string transformFile);

  void initialize(double **data_, double **pos_data_);

  FrameSkel(double **data_, double **pos_data_, string transformFile);

  FrameSkel(double **data_, double **pos_data_);

  FrameSkel(double **data_, double **pos_data_, string transformFile, int fid);

  FrameSkel() {}

  ~FrameSkel() {}
};

#endif  // FEATURE_GENERATION_PCL_SRC_FRAME_SKEL_H_
