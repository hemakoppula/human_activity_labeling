/*
Copyright (C) 2012 Hema Koppula
*/


#ifndef FEATURE_GENERATION_PCL_SRC_INCLUDES_COMBINEUTILS_H_
#define FEATURE_GENERATION_PCL_SRC_INCLUDES_COMBINEUTILS_H_

#include <boost/numeric/ublas/matrix.hpp>
#include <boost/numeric/ublas/io.hpp>
#include <string>
#include <vector>
#include <iostream>
#include "pcl/features/normal_3d.h"


using namespace std;

#define PI (3.141592653589793)



void transformPointCloud(boost::numeric::ublas::matrix<double> &transform,
                         pcl::PointCloud<pcl::PointXYZRGB>::Ptr in,
                         pcl::PointCloud<pcl::PointXYZRGB>::Ptr out) {
  boost::numeric::ublas::matrix<double> matIn(4, 1);
  *out = *in;

  for (size_t i = 0; i < in->points.size(); ++i) {
    double * matrixPtr = matIn.data().begin();

    matrixPtr[0] = in->points[i].x;
    matrixPtr[1] = in->points[i].y;
    matrixPtr[2] = in->points[i].z;
    matrixPtr[3] = 1;
    boost::numeric::ublas::matrix<double> matOut = prod(transform, matIn);
    matrixPtr = matOut.data().begin();

    out->points[i].x = matrixPtr[0];
    out->points[i].y = matrixPtr[1];
    out->points[i].z = matrixPtr[2];
  }
}


float sqrG(float y) {
  return y*y;
}

class VectorG {
 public:
  double v[3];

  VectorG() {}

  VectorG(double unitX, double unitY, double unitZ) {
    v[0] = unitX;
    v[1] = unitY;
    v[2] = unitZ;
  }

  explicit VectorG(pcl::PointXYZRGBNormal p) {
    v[0] = p.x;
    v[1] = p.y;
    v[2] = p.z;
  }

  explicit VectorG(pcl::PointXYZRGB p) {
    v[0] = p.x;
    v[1] = p.y;
    v[2] = p.z;
  }

  explicit VectorG(pcl::PointXYZRGBCamSL p) {
    v[0] = p.x;
    v[1] = p.y;
    v[2] = p.z;
  }

  /**
   * compute the distance from the line joining p1 and p2
   */
  double computeDistanceSqrFromLine(VectorG p1, VectorG p2) {
    VectorG t1 = p1.subtract(*this);
    VectorG t2 = p2.subtract(p1);
    return (t1.getNormSqr() * t2.getNormSqr() - sqrG(t1.dotProduct(t2)))
              / t2.getNormSqr();
  }

  /**
   *true iff it lies in the cylinder of infinite radius defined by p1 and p2
   * the line segment (p1,p2) is the axis of this cylinder
   */
  bool isInsideLineSegment(VectorG p1, VectorG p2) {
  VectorG lineSeg = p1.subtract(p2);
  double lengthSqr = lineSeg.getNormSqr();
  VectorG p1Seg = subtract(p1);
  VectorG p2Seg = subtract(p2);

  if (p1Seg.getNormSqr() <= lengthSqr && p2Seg.getNormSqr() <= lengthSqr)
    return true;
  else
    return false;
  }

  void normalize() {
    double norm = getNorm();
    for (int i = 0; i < 3; i++)
      v[i] = v[i] / norm;
  }

  VectorG normalizeAndReturn() const {
      VectorG out;
      double norm = getNorm();
      for (int i = 0; i < 3; i++)
          out.v[i] = v[i] / norm;
      return out;
  }

  pcl::PointXYZRGB getAsPoint() {
    pcl::PointXYZRGB p;
    p.x = v[0];
    p.y = v[1];
    p.z = v[2];
    return p;
  }

  double getNorm() const {
    return sqrt(getNormSqr());
  }

  double getNormSqr() const {
    return (sqrG(v[0]) + sqrG(v[1]) + sqrG(v[2]));
  }

  double dotProduct(VectorG v2g) {
    double sum = 0;
    for (int i = 0; i < 3; i++)
      sum = sum + v[i] * v2g.v[i];
    return sum;
  }

  VectorG multiply(double scalar) {
    VectorG out;
    for (int i = 0; i < 3; i++)
      out.v[i] = scalar*v[i];
    return out;
  }

  VectorG subtract(VectorG v2g) {
    VectorG out;
    for (int i = 0; i < 3; i++)
      out.v[i] = v[i] - v2g.v[i];
    return out;
  }


  VectorG add(VectorG v2g) {
    VectorG out;
    for (int i = 0; i < 3; i++)
      out.v[i] = v[i] + v2g.v[i];
    return out;
  }

  float eucliedianDistance(VectorG v2g) {
    float sum = 0;
    for (int i = 0; i < 3; i++)
      sum = sum + sqrG(v[i] - v2g.v[i]);
    return sqrt(sum);
  }

  Eigen::Vector4f   toEigenFormat() {
    Eigen::Vector4f out;
    for (int i = 0; i < 3; i++)
      out(i) = v[i];
    return out;
  }
};

boost::numeric::ublas::matrix<double>
transformAsMatrix(double *mv, double *origin) {
  boost::numeric::ublas::matrix<double> outMat(4, 4);
  outMat(0, 0) = mv[0];
  outMat(0, 1) = mv[6];
  outMat(0, 2) = mv[3];
  outMat(1, 0) = mv[2];
  outMat(1, 1) = mv[8];
  outMat(1, 2) = mv[5];
  outMat(2, 0) = mv[1];
  outMat(2, 1) = mv[7];
  outMat(2, 2) = mv[4];

  outMat(3, 0) = outMat(3, 1) = outMat(3, 2) = 0;
  outMat(0, 3) = origin[0];
  outMat(1, 3) = origin[2];
  outMat(2, 3) = origin[1];
  outMat(3, 3) = 1;

  return outMat;
}

class TransformG {
 public:
  void writefile(string filename) {
    std::ofstream outFile;
    outFile.open(filename.c_str());
    outFile << transformMat(0, 0) << "," << transformMat(0, 1) << ","
              << transformMat(0, 2) << "," << transformMat(0, 3) << endl;
    outFile << transformMat(1, 0) << "," << transformMat(1, 1) << ","
              << transformMat(1, 2) << "," << transformMat(1, 3) << endl;
    outFile << transformMat(2, 0) << "," << transformMat(2, 1) << ","
              << transformMat(2, 2) << "," << transformMat(2, 3) << endl;
    outFile << transformMat(3, 0) << "," << transformMat(3, 1) << ","
              << transformMat(3, 2) << "," << transformMat(3, 3) << endl;
    outFile.close();
  }

  void transformPointCloudInPlaceAndSetOrigin(pcl::PointCloud<pcl::PointXYZRGB> & in) {
    boost::numeric::ublas::matrix<double> matIn(4, 1);

    for (size_t i = 0; i < in.points.size(); ++i) {
      double * matrixPtr = matIn.data().begin();

      matrixPtr[0] = in.points[i].x;
      matrixPtr[1] = in.points[i].y;
      matrixPtr[2] = in.points[i].z;
      matrixPtr[3] = 1;
      boost::numeric::ublas::matrix<double> matOut = prod(transformMat, matIn);
      matrixPtr = matOut.data().begin();

      in.points[i].x = matrixPtr[0];
      in.points[i].y = matrixPtr[1];
      in.points[i].z = matrixPtr[2];
    }

    in.sensor_origin_ = getOrigin().toEigenFormat();
  }

  void transformPointInPlace(pcl::PointXYZRGB & in) {
    boost::numeric::ublas::matrix<double> matIn(4, 1);

    double * matrixPtr = matIn.data().begin();

    matrixPtr[0] = in.x;
    matrixPtr[1] = in.y;
    matrixPtr[2] = in.z;
    matrixPtr[3] = 1;
    boost::numeric::ublas::matrix<double> matOut = prod(transformMat, matIn);
    matrixPtr = matOut.data().begin();

    in.x = matrixPtr[0];
    in.y = matrixPtr[1];
    in.z = matrixPtr[2];
  }

  void transformPointInPlace(pcl::PointXYZ & in) {
    boost::numeric::ublas::matrix<double> matIn(4, 1);

    double * matrixPtr = matIn.data().begin();

    matrixPtr[0] = in.x;
    matrixPtr[1] = in.y;
    matrixPtr[2] = in.z;
    matrixPtr[3] = 1;
    boost::numeric::ublas::matrix<double> matOut = prod(transformMat, matIn);
    matrixPtr = matOut.data().begin();

    in.x = matrixPtr[0];
    in.y = matrixPtr[1];
    in.z = matrixPtr[2];
  }

  boost::numeric::ublas::matrix<double> transformMat;

  explicit TransformG(boost::numeric::ublas::matrix<double> &mat) {
      transformMat = mat;
  }


  TransformG(double *orie, double *pos) {
    transformMat = transformAsMatrix(orie, pos);
  }

  TransformG postMultiply(TransformG multiplicand) {
    TransformG out;
    out.transformMat = boost::numeric::ublas::prod(transformMat,
                                                   multiplicand.transformMat);
    return out;
  }

  bool isOverlapSignificant(TransformG other) {
    VectorG orig1 = getOrigin();
    VectorG orig2 = other.getOrigin();
    VectorG disp = orig1.subtract(orig2);
    if (disp.getNormSqr() > 0.5)  // if the camera moved by more than 40 cm
        return false;
    double angle = 34;
    double cosTurn = fabs(getZUnitVector().dotProduct(other.getZUnitVector()));
    std::cerr << "turn by" << cosTurn << std::endl;
    // if the camera turned by more than "angle"
    if (cosTurn < cos(angle * PI / 180.0))
      return false;

    return true;
  }

  explicit TransformG(double *vo) {
    transformMat.resize(4, 4);
    for (int r = 0; r < 4; r++) {
      for (int c = 0; c < 4; c++) {
        transformMat(r, c) = vo[r*4+c];
      }
    }
  }

  explicit TransformG(vector<double> &vo) {
    transformMat.resize(4, 4);
    for (int r = 0; r < 4; r++) {
      for (int c = 0; c < 4; c++) {
          transformMat(r, c) = vo.at(r*4 + c);
      }
    }
  }

  TransformG inverse() const {
    double vi[16];
    double vo[16];
    for (int r = 0; r < 4; r++) {
      for   (int c = 0; c < 4; c++) {
        vi[r*4+c] = transformMat(r, c);
      }
    }
    cout << "mat is :" << endl;
    print();

    gluInvertMatrix(vi, vo);
    TransformG retmat(vo);
    cout << "inversen is:" << endl;
    return retmat;
  }

  static bool gluInvertMatrix(const double m[16], double invOut[16]) {
    double inv[16], det;
    int i;

    inv[0] = m[5] * m[10] * m[15] - m[5] * m[11] * m[14] - m[9] * m[6] * m[15]
            + m[9] * m[7] * m[14] + m[13] * m[6] * m[11] - m[13] * m[7] * m[10];
    inv[4] = -m[4] * m[10] * m[15] + m[4] * m[11] * m[14] + m[8] * m[6] * m[15]
            - m[8] * m[7] * m[14] - m[12] * m[6] * m[11] + m[12] * m[7] * m[10];
    inv[8] = m[4] * m[9] * m[15] - m[4] * m[11] * m[13] - m[8] * m[5] * m[15]
            + m[8] * m[7] * m[13] + m[12] * m[5] * m[11] - m[12] * m[7] * m[9];
    inv[12] = -m[4] * m[9] * m[14] + m[4] * m[10] * m[13] + m[8] * m[5] * m[14]
            - m[8] * m[6] * m[13] - m[12] * m[5] * m[10] + m[12] * m[6] * m[9];
    inv[1] = -m[1] * m[10] * m[15] + m[1] * m[11] * m[14] + m[9] * m[2] * m[15]
            - m[9] * m[3] * m[14] - m[13] * m[2] * m[11] + m[13] * m[3] * m[10];
    inv[5] = m[0] * m[10] * m[15] - m[0] * m[11] * m[14] - m[8] * m[2] * m[15]
            + m[8] * m[3] * m[14] + m[12] * m[2] * m[11] - m[12] * m[3] * m[10];
    inv[9] = -m[0] * m[9] * m[15] + m[0] * m[11] * m[13] + m[8] * m[1] * m[15]
            - m[8] * m[3] * m[13] - m[12] * m[1] * m[11] + m[12] * m[3] * m[9];
    inv[13] = m[0] * m[9] * m[14] - m[0] * m[10] * m[13] - m[8] * m[1] * m[14]
            + m[8] * m[2] * m[13] + m[12] * m[1] * m[10] - m[12] * m[2] * m[9];
    inv[2] = m[1] * m[6] * m[15] - m[1] * m[7] * m[14] - m[5] * m[2] * m[15]
            + m[5] * m[3] * m[14] + m[13] * m[2] * m[7] - m[13] * m[3] * m[6];
    inv[6] = -m[0] * m[6] * m[15] + m[0] * m[7] * m[14] + m[4] * m[2] * m[15]
            - m[4] * m[3] * m[14] - m[12] * m[2] * m[7] + m[12] * m[3] * m[6];
    inv[10] = m[0] * m[5] * m[15] - m[0] * m[7] * m[13] - m[4] * m[1] * m[15]
            + m[4] * m[3] * m[13] + m[12] * m[1] * m[7] - m[12] * m[3] * m[5];
    inv[14] = -m[0] * m[5] * m[14] + m[0] * m[6] * m[13] + m[4] * m[1] * m[14]
            - m[4] * m[2] * m[13] - m[12] * m[1] * m[6] + m[12] * m[2] * m[5];
    inv[3] = -m[1] * m[6] * m[11] + m[1] * m[7] * m[10] + m[5] * m[2] * m[11]
            - m[5] * m[3] * m[10] - m[9] * m[2] * m[7] + m[9] * m[3] * m[6];
    inv[7] = m[0] * m[6] * m[11] - m[0] * m[7] * m[10] - m[4] * m[2] * m[11]
            + m[4] * m[3] * m[10] + m[8] * m[2] * m[7] - m[8] * m[3] * m[6];
    inv[11] = -m[0] * m[5] * m[11] + m[0] * m[7] * m[9] + m[4] * m[1] * m[11]
            - m[4] * m[3] * m[9] - m[8] * m[1] * m[7] + m[8] * m[3] * m[5];
    inv[15] = m[0] * m[5] * m[10] - m[0] * m[6] * m[9] - m[4] * m[1] * m[10]
            + m[4] * m[2] * m[9] + m[8] * m[1] * m[6] - m[8] * m[2] * m[5];

    det = m[0] * inv[0] + m[1] * inv[4] + m[2] * inv[8] + m[3] * inv[12];

    if (det == 0)
      return false;

    det = 1.0 / det;

    for (i = 0; i < 16; i++)
      invOut[i] = inv[i] * det;

    return true;
  }

  TransformG preMultiply(TransformG multiplicand) {
    TransformG out;
    out.transformMat = boost::numeric::ublas::prod(multiplicand.transformMat,
                                                 transformMat);
    return out;
  }

  TransformG() {
    transformMat = boost::numeric::ublas::matrix<double>(4, 4);
  }

  float getDistanceFromOrigin(VectorG point) {
    return point.eucliedianDistance(getOrigin());
  }

  VectorG getXUnitVector() {
    return getIthColumn(0);
  }

  VectorG getYUnitVector() {
    return getIthColumn(1);
  }

  VectorG getZUnitVector() {
    return getIthColumn(2);
  }

  VectorG getIthColumn(int i) {
    return VectorG(transformMat(0, i), transformMat(1, i), transformMat(2, i));
  }

  VectorG getOrigin() {
    return VectorG(transformMat(0, 3), transformMat(1, 3), transformMat(2, 3));
  }

  bool isPointVisible(VectorG vPoint) {
    VectorG cam2PointRay = vPoint.subtract(getOrigin());
    if (cam2PointRay.getNormSqr() > 16.0)
      return false;
    cam2PointRay.normalize();
    VectorG cam2PointRayUnit = cam2PointRay;
    double xDot = cam2PointRayUnit.dotProduct(getXUnitVector());
    double yDot = cam2PointRayUnit.dotProduct(getYUnitVector());
    double zDot = cam2PointRayUnit.dotProduct(getZUnitVector());
    if ( zDot > 0 && fabs(xDot/zDot) < 0.51 && fabs(yDot/zDot) < 0.4)
      return true;
    else
      return false;
  }

  void filterPeripheryCloud() {}

  void
  print() const {
    for (int i = 0; i < 4; i++) {
      for (int j = 0; j < 4; j++)
        std::cerr << transformMat(i, j) << ",";
      std::cerr << std::endl;
    }
  }
};

TransformG readTranform(const string & filename) {
  boost::numeric::ublas::matrix<double> mat(4, 4);
  ifstream file((char*)filename.c_str(), ifstream::in);
  string line;
  int row = 0;
  while (getline(file, line)) {
    string e1;
    stringstream lineStream(line);
    int col = 0;
    while (getline(lineStream, e1, ',')) {
      mat(row, col) = atof(e1.c_str());
      col += 1;
    }
    row += 1;
  }
  TransformG transG(mat);
  return transG;
}

void appendCamIndex(pcl::PointCloud<pcl::PointXYZRGB>::Ptr in,
                    pcl::PointCloud<pcl::PointXYGRGBCam>::Ptr out,
                    int camIndex) {
  out->header = in->header;
  out->points.resize(in->size());
  for (unsigned int i=0; i < in->size(); i++) {
      out->points[i].x = in->points[i].x;
      out->points[i].y = in->points[i].y;
      out->points[i].z = in->points[i].z;
      out->points[i].rgb = in->points[i].rgb;
      out->points[i].cameraIndex = camIndex;
  }
}

void appendCamIndexAndDistance(pcl::PointCloud<pcl::PointXYZRGBNormal>::Ptr in,
                               pcl::PointCloud<pcl::PointXYGRGBCam>::Ptr out,
                               int camIndex, VectorG camOrigin) {
  out->header = in->header;
  out->points.resize(in->size());
  for (unsigned int i = 0; i < in->size(); i++) {
    out->points[i].x = in->points[i].x;
    out->points[i].y = in->points[i].y;
    out->points[i].z = in->points[i].z;
    out->points[i].rgb = in->points[i].rgb;
    out->points[i].normal_x = in->points[i].normal_x;
    out->points[i].normal_y = in->points[i].normal_y;
    out->points[i].normal_z = in->points[i].normal_z;
    out->points[i].cameraIndex = camIndex;
    VectorG pt(in->points[i]);
    VectorG disp = pt.subtract(camOrigin);
    out->points[i].distance = disp.getNorm();
  }
}

void appendCamIndexAndDistance(pcl::PointCloud<pcl::PointXYZRGB>::Ptr in,
                               pcl::PointCloud<pcl::PointXYZRGBCamSL>::Ptr out,
                               int camIndex, VectorG camOrigin) {
  out->points.resize(in->size());
  for (unsigned int i = 0; i < in->size(); ++i) {
    out->points[i].x = in->points[i].x;
    out->points[i].y = in->points[i].y;
    out->points[i].z = in->points[i].z;
    out->points[i].rgb = in->points[i].rgb;
    out->points[i].cameraIndex = camIndex;
    VectorG pt(in->points[i]);
    VectorG disp = pt.subtract(camOrigin);
    out->points[i].distance = disp.getNorm();
  }
}

double cosNormal(pcl::PointXYZRGBNormal p1, pcl::PointXYZRGBNormal p2) {
  return fabs( p1.normal_x * p2.normal_x
               + p1.normal_y * p2.normal_y
               + p1.normal_z  * p2.normal_z);
}

#ifdef __cplusplus
extern "C" {
#endif

#ifdef __cplusplus
}
#endif

#endif  // FEATURE_GENERATION_PCL_SRC_INCLUDES_COMBINEUTILS_H_
