

#include "constants.h"
#include "includes/color.cpp"


#include "includes/point_types.h"
#include "readData.cpp"
typedef pcl::PointXYZRGB PointT;

#include "includes/CombineUtils.h"
#include "frame_skel.h"
#include <pcl/visualization/pcl_visualizer.h>


pcl::PointCloud<PointT>::Ptr cloudPtr (new pcl::PointCloud<PointT>);


double head_ori[9];
double head_pos[3];


void createPointCloud(int ***IMAGE, pcl::PointCloud<PointT>& cloud ) {
    int index = 0;
    ColorRGB color(0, 0, 0);

    cloud.height = 1;
    cloud.width = X_RES*Y_RES;
    cloud.points.resize(cloud.height * cloud.width);

    for (int y = 0; y < Y_RES; y++) {
        for (int x = 0; x < X_RES; x++) {

            if(IMAGE[x][y][3] != 0) {
            	color.assignColor(float(IMAGE[x][y][0])/255.0,float(IMAGE[x][y][1])/255,float(IMAGE[x][y][2])/255);
            	cloud.points.at(index).z = IMAGE[x][y][3]; //*0.001f;
            	cloud.points.at(index).x = ( x  - X_RES*0.5) * cloud.points.at(index).z * 1.1147/640;
            	cloud.points.at(index).y = (  Y_RES*0.5 -y) * cloud.points.at(index).z* 0.8336/480 ;
           	cloud.points.at(index).rgb = color.getFloatRep();
	    } else {
	        color.assignColor(float(IMAGE[x][y][0])/255.0,float(IMAGE[x][y][1])/255,float(IMAGE[x][y][2])/255);
            	cloud.points.at(index).y = std::numeric_limits<float>::quiet_NaN ();
            	cloud.points.at(index).x = std::numeric_limits<float>::quiet_NaN ();
            	cloud.points.at(index).z = std::numeric_limits<float>::quiet_NaN ();
                cloud.points.at(index).rgb = color.getFloatRep();
	    }
            index++;
        }
    }

}

void createPointCloud(int ***IMAGE, string transformfile,pcl::PointCloud<PointT>& cloud ) {
    int index = 0;
    ColorRGB color(0, 0, 0);

    cloud.height = 1;
    cloud.width = X_RES*Y_RES;
    cloud.points.resize(cloud.height * cloud.width);

    for (int y = 0; y < Y_RES; y++) {
        for (int x = 0; x < X_RES; x++) {
            if(IMAGE[x][y][3] != 0) {
            	color.assignColor(float(IMAGE[x][y][0])/255.0,float(IMAGE[x][y][1])/255,float(IMAGE[x][y][2])/255);
            	cloud.points.at(index).y = IMAGE[x][y][3]; //*0.001f;
            	cloud.points.at(index).x = ( x  - X_RES*0.5) * cloud.points.at(index).y * 1.1147/640;
            	cloud.points.at(index).z = (  Y_RES*0.5 -y) * cloud.points.at(index).y* 0.8336/480 ;
           	cloud.points.at(index).rgb = color.getFloatRep();
	    } else {
	        color.assignColor(float(IMAGE[x][y][0])/255.0,float(IMAGE[x][y][1])/255,float(IMAGE[x][y][2])/255);
            	cloud.points.at(index).y = 0;//std::numeric_limits<float>::quiet_NaN ();
            	cloud.points.at(index).x = 0; // std::numeric_limits<float>::quiet_NaN ();
            	cloud.points.at(index).z = 0;//std::numeric_limits<float>::quiet_NaN ();
                cloud.points.at(index).rgb = color.getFloatRep();
	    }


            index++;
        }
    }
    TransformG globalTransform;
    globalTransform = readTranform(transformfile);
    globalTransform.transformPointCloudInPlaceAndSetOrigin(cloud);



}


void drawUpperSkeleton(double **data, double **pos_data, string transformfile, boost::shared_ptr<pcl::visualization::PCLVisualizer> &p) {
    TransformG globalTransform;
    globalTransform = readTranform(transformfile);
    FrameSkel sf (data, pos_data,transformfile);
    vector<PointT> points;
    for (size_t i = 0; i < sf.transformed_joints.size(); i++) {

        std::stringstream ss;
        ss << "j" << i;
        cout << "adding joint " << ss.str() << endl;
        p->addSphere(sf.transformed_joints.at(i), 10, 1, 0, 0, ss.str(), 0);
    }

    p->addLine(sf.transformed_joints.at(0), sf.transformed_joints.at(1), 1, 0, 0, "e1", 0);
    p->addLine(sf.transformed_joints.at(1), sf.transformed_joints.at(2), 1, 0, 0, "e2", 0);
    p->addLine(sf.transformed_joints.at(1), sf.transformed_joints.at(5), 1, 0, 0, "e3", 0);
    p->addLine(sf.transformed_joints.at(1), sf.transformed_joints.at(3), 1, 0, 0, "e4", 0);
    p->addLine(sf.transformed_joints.at(3), sf.transformed_joints.at(4), 1, 0, 0, "e5", 0);
    p->addLine(sf.transformed_joints.at(5), sf.transformed_joints.at(6), 1, 0, 0, "e6", 0);
    p->addLine(sf.transformed_joints.at(6), sf.transformed_joints.at(8), 1, 0, 0, "e7", 0);
    p->addLine(sf.transformed_joints.at(4), sf.transformed_joints.at(7), 1, 0, 0, "e8", 0);


}

void drawSkeleton(double **data, double **pos_data, string transformfile, boost::shared_ptr<pcl::visualization::PCLVisualizer> & p) {
    TransformG globalTransform;
    globalTransform = readTranform(transformfile);

    vector<PointT> points;
    for (int i = 0; i < JOINT_NUM; i++) {
        PointT p1;
        p1.x = data[i][9];
        p1.y = data[i][11];
        p1.z = data[i][10];
        globalTransform.transformPointInPlace(p1);
        points.push_back(p1);
        std::stringstream ss;
        ss << "j" << i;
        cout << "adding joint " << ss.str() << endl;
        p->addSphere(p1, 10, 1, 0, 0, ss.str(), 0);
    }
    for (int i = 0; i < POS_JOINT_NUM; i++) {
        PointT p1;
        p1.x = pos_data[i][0];
        p1.y = pos_data[i][2];
        p1.z = pos_data[i][1];
        globalTransform.transformPointInPlace(p1);
        points.push_back(p1);
        std::stringstream ss;
        ss << "j" << i + JOINT_NUM;
        cout << "adding joint " << ss.str() << endl;
        p->addSphere(p1, 10, 1, 0, 0, ss.str(), 0);
    }

    p->addLine(points.at(0), points.at(1), 1, 0, 0, "e1", 0);
    p->addLine(points.at(1), points.at(2), 1, 0, 0, "e2", 0);

    p->addLine(points.at(1), points.at(3), 1, 0, 0, "e3", 0);
    p->addLine(points.at(3), points.at(4), 1, 0, 0, "e4", 0);
    p->addLine(points.at(1), points.at(5), 1, 0, 0, "e5", 0);
    p->addLine(points.at(5), points.at(6), 1, 0, 0, "e6", 0);
    p->addLine(points.at(7), points.at(8), 1, 0, 0, "e7", 0);
    p->addLine(points.at(9), points.at(10), 1, 0, 0, "e8", 0);
    p->addLine(points.at(10), points.at(14), 1, 0, 0, "e9", 0);
    p->addLine(points.at(8), points.at(13), 1, 0, 0, "e10", 0);

    p->addLine(points.at(6), points.at(12), 1, 0, 0, "e11", 0);
    p->addLine(points.at(4), points.at(11), 1, 0, 0, "e12", 0);

    p->addLine(points.at(2), points.at(7), 1, 0, 0, "e13", 0);
    p->addLine(points.at(2), points.at(9), 1, 0, 0, "e14", 0);
}


int
main(int argc, char **argv) {
    srand(time(0));
    boost::shared_ptr<pcl::visualization::PCLVisualizer> p (new pcl::visualization::PCLVisualizer ("3D Viewer"));

    //pcl::visualization::PCLVisualizer p("test");

    string transformfile = (string)argv[1]+(string)argv[2]+"_globalTransform.txt";
    double **data; //[JOINT_NUM][JOINT_DATA_NUM];
    int **data_CONF; //[JOINT_NUM][JOINT_DATA_TYPE_NUM]
    double **pos_data; //[POS_JOINT_NUM][POS_JOINT_DATA_NUM];
    int *pos_data_CONF; //[POS_JOINT_NUM]
    data = new double*[JOINT_NUM];
    data_CONF = new int*[JOINT_NUM];
    for (int i = 0; i < JOINT_NUM; i++) {
        data[i] = new double[JOINT_DATA_NUM];
        data_CONF[i] = new int[JOINT_DATA_TYPE_NUM];
    }
    pos_data = new double*[POS_JOINT_NUM];
    pos_data_CONF = new int[POS_JOINT_NUM];
    for (int i = 0; i < POS_JOINT_NUM; i++) {
        pos_data[i] = new double[POS_JOINT_DATA_NUM];
    }

    int ***IMAGE; // [X_RES][Y_RES]
    IMAGE = new int**[X_RES];
    for (int i = 0; i < X_RES; i++) {
        IMAGE[i] = new int*[Y_RES];
        for (int j = 0; j < Y_RES; j++) {
            IMAGE[i][j] = new int[RGBD_data];
        }
    }




    vector <string> fileList;
    vector<vector<double> > objData;
    readData* DATA = new readData((string)argv[1], (string)argv[2], false, fileList);
    for (int i = 0; i < atoi(argv[3]) - 1; i++) {
        int status = DATA->readNextFrame(data, pos_data, data_CONF, pos_data_CONF, IMAGE, objData); //DATA->skipNextFrame();
    }
    int status = DATA->readNextFrame(data, pos_data, data_CONF, pos_data_CONF, IMAGE, objData);

    //Frame frame(IMAGE, data, pos_data, objData,argv[2], status, transformfile);
    if (status != atoi(argv[3])) {
        cout << "ERROR frame number not present!!" << endl;
    }

    for (int i = 0; i < 9; i++) {
        head_ori[i] = data[HEAD_JOINT_NUM][i];
    }

    for (int i = 0; i < 3; i++) {
        head_pos[i] = data[HEAD_JOINT_NUM][i + 9];
    }
    createPointCloud(IMAGE, transformfile, *cloudPtr);
    //pcl::PointXYZ pt(0,0,1000);
    //p->addSphere(pt, 10, 1, 0, 0, "test", 0);
    drawSkeleton(data, pos_data, transformfile, p);
    p->setBackgroundColor(1, 1, 1);


    std::cerr << "PointCloudColorHandlerRGBField demo." << std::endl;

    pcl::visualization::PointCloudColorHandlerRGBField<PointT> handler(cloudPtr);



    p->addPointCloud(cloudPtr, handler, "cloud_rgb", 0);
    p->addCoordinateSystem(1000, 0);
    while (!p->wasStopped()) {
        p->spinOnce(1000); // Give the GUI 1000ms to handle events, then return
    }
    p->removePointCloud("cloud_rgb");

}
/**
there are 11 joints that have both orientation (3x3) and position (x,y,z) data
        XN_SKEL_HEAD,0
        XN_SKEL_NECK,1
        XN_SKEL_TORSO,2
        XN_SKEL_LEFT_SHOULDER,3
        XN_SKEL_LEFT_ELBOW,4
        XN_SKEL_RIGHT_SHOULDER,5
        XN_SKEL_RIGHT_ELBOW,6
        XN_SKEL_LEFT_HIP,7
        XN_SKEL_LEFT_KNEE,8
        XN_SKEL_RIGHT_HIP,9
        XN_SKEL_RIGHT_KNEE,10

there are 4 joints that have only position (x,y,z) data
        XN_SKEL_LEFT_HAND,11
        XN_SKEL_RIGHT_HAND,12
        XN_SKEL_LEFT_FOOT,13
        XN_SKEL_RIGHT_FOOT,14

 data[][0~8]    -> orientation (3x3 matrix)
                     3x3 matrix is stored as
                        0 1 2
                        3 4 5
                        6 7 8
                     read PDF for description about 3x3 matrix
 data[][9~11]   -> x,y,z position for eleven joints

 data_CONF[][0]   -> confidence value of orientation  (data[][0~8])
 data_CONF[][1]   -> confidence value of xyz position (data[][9~11])

 data_pos[][0~2] -> x,y,z position for four joints
 data_pos_CONF[]  -> confidence value of xyz position (data_pos[][0~2])

X_RES and Y_RES are in constants.h, so just use them.
 IMAGE[X_RES][Y_RES][0~2]   -> RGB values
 IMAGE[X_RES][Y_RES][3]     -> depth values


 */
