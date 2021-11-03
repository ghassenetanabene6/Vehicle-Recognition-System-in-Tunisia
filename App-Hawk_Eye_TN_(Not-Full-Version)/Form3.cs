using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.Text;
using System.Windows.Forms;
using AForge.Video;
using AForge.Video.DirectShow;
using System.Threading;

using Emgu.CV;
using Emgu.CV.Structure;

namespace Hawk_Eye_App
{
    public partial class Form3 : Form
    {
        VideoCaptureDevice device;
        FilterInfoCollection filter;
        //bool confirmation;
        int i ;

        public Form3()
        {
            InitializeComponent();
        }
        
        public Form3(FilterInfoCollection filter)
        {
            this.filter = filter;
            //this.confirmation = false;
            this.i = 0;
        }
        private void Form3_Load(object sender, EventArgs e)
        {
            filter = new FilterInfoCollection(FilterCategory.VideoInputDevice);
            foreach (FilterInfo device in filter)
                comboBox_device.Items.Add(device.Name);

            comboBox_device.SelectedIndex = 0;

        }

        private void Form3_FormClosing(object sender, FormClosingEventArgs e)
        {   try
            {
                if (device.IsRunning)
                {
                    device.SignalToStop();
                    device.WaitForStop();
                }
                
            }
            catch
            { }
        }

        //Recognition based on python AI models in backend

        private string vehicle_recognition(string image_path)
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


        // Making new frame to keep the video capture running

        private void Device_NewFrame(object sender, NewFrameEventArgs eventArgs)
        {
            Bitmap bitmap = (Bitmap)eventArgs.Frame.Clone();
            pictureBox1.Image = bitmap;
            pictureBox1.SizeMode = PictureBoxSizeMode.StretchImage;
        }

        // This procedure will be used to give the vehicle recognition result 

        private void Recognition_Result_Frame(object sender, NewFrameEventArgs eventArgs)
        {
            Bitmap bitmap = (Bitmap)eventArgs.Frame.Clone();
            string frame_name = @"D:\\frame_name.jpg";
            
            bitmap.Save(frame_name, System.Drawing.Imaging.ImageFormat.Jpeg);

            //string output = vehicle_recognition(frame_name);
            string output = @"D:\\avatargt.jpg";
            Bitmap bit = new Bitmap(output);
            
            //Bitmap bit = new Bitmap(@"D:\\lol.jpg");
            pictureBox1.Image = bit;
            pictureBox1.SizeMode = PictureBoxSizeMode.StretchImage;
            device = null;
        }
        

        //Button to start video capture through camera

        private void btn_Camera_Click(object sender, EventArgs e)
        {
            i = i + 1;
            device = new VideoCaptureDevice(filter[comboBox_device.SelectedIndex].MonikerString);
            device.NewFrame += Device_NewFrame;
            device.Start();
            MessageBox.Show(i.ToString());
            /*Button btnSender = (Button)sender;
           if (btnSender == btn_Deny)
            {
            }*/
        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {
        }

        private void comboBox_device_SelectedIndexChanged(object sender, EventArgs e)
        {
        }


        //Recognition button
        private void btn_recognition_Click(object sender, EventArgs e)
        {
            device.SignalToStop();
            device.WaitForStop();
            device.NewFrame += Recognition_Result_Frame;
            //device.pause();

        }

        //confirm the recognition result and move on to the next form
        private void btn_Confirm_Click(object sender, EventArgs e)
        { 
            Form1 f1 = new Form1();
            f1.Show();
            this.Hide();

        }

        //Deny the recognition result and repeat the process
        private void btn_Deny_Click(object sender, EventArgs e)
        {
            //btn_Camera_Click(sender,e);
            device.SignalToStop();
            device.WaitForStop();
        }
    }
}
