using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using VisioForge.Shared.DirectShowLib;
using System.Threading;
using System.Diagnostics;

namespace Hawk_Eye_App
{
    public partial class Form2 : Form
    {
        public Form2()
        {
            InitializeComponent();

        }

        private string run_cmd(string image_path)
        {
            string fileName = @"D:\\Hawk_Eye_version_1.0_LP_recog\\Hawk_Eye_version_1.0_LP_recog\\main_vehicle_to_LP.py";

            Process p = new Process();
            p.StartInfo = new ProcessStartInfo(@"D:\LOGICIELS\pythonn\WPy64-3740\python-3.7.4.amd64\python.exe")
            {
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true,

            };

            p.StartInfo.Arguments = string.Format("{0} --image={1}", fileName, image_path);
            p.Start();

            string output = p.StandardOutput.ReadToEnd();
            p.WaitForExit();

            string result = output.Substring(0, output.Length - 2);
            return (result);
        }


        private void videoCapture1_Paint(object sender, PaintEventArgs e)
        {

        }
        private void TakeFrame()
        {
            //videoCapture1.Frame_Save(Environment.GetFolderPath(Environment.SpecialFolder.MyPictures) + "\\frame.jpg", VisioForge.Types.VFImageFormat.JPEG, 85);
            videoCapture1.Frame_Save(@"D:\\Hawk_Eye_version_1.0_LP_recog\\Hawk_Eye_version_1.0_LP_recog\\frame.jpg", VisioForge.Types.VFImageFormat.JPEG, 85);
            Thread.Sleep(2000);
            
        }



        private void TakePhoto_Click(object sender, EventArgs e)
        {
            string path_to_frame = "D:\\Hawk_Eye_version_1.0_LP_recog\\Hawk_Eye_version_1.0_LP_recog\\frame.jpg";
            videoCapture1.Frame_Save(path_to_frame, VisioForge.Types.VFImageFormat.JPEG, 85);
            string output = run_cmd(path_to_frame);
            Bitmap bit = new Bitmap(output);
            pictureBox1.Image = bit;
            pictureBox1.SizeMode = PictureBoxSizeMode.StretchImage;

        }

        private void StopCam_Click(object sender, EventArgs e)
        {
            videoCapture1.Stop();
        }

        private void StartCam_Click(object sender, EventArgs e)
        {
            videoCapture1.Video_CaptureDevice = videoCapture1.Video_CaptureDevicesInfo[0].Name;
            //videoCapture1.Audio_CaptureDevice = videoCapture1.Audio_CaptureDevicesInfo[0].Name;
            videoCapture1.Mode = VisioForge.Types.VFVideoCaptureMode.VideoPreview;
            videoCapture1.Start();
            //while (true)
            //{
                //TakeFrame();
            //}

        }
    }
}
