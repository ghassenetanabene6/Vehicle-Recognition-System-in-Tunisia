using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Diagnostics;
using System.IO;

namespace Hawk_Eye_App
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            OpenFileDialog ofd = new OpenFileDialog();
            if (ofd.ShowDialog() == DialogResult.OK)
            {
                string output = run_cmd(ofd.FileName);
                //string output = @"D:\\Hawk_Eye_version_1.0_LP_recog\\Hawk_Eye_version_1.0_LP_recog\\623.jpg";
                Bitmap bit = new Bitmap(output);
                pictureBox1.Image = bit;
                pictureBox1.SizeMode = PictureBoxSizeMode.StretchImage;
                //MessageBox.Show(output);
                //MessageBox.Show(ofd.FileName);
                //run_cmd(ofd.FileName);



            }

        }
        private string run_cmd(string image_path)
        {
            //string fileName = @"D:\\Hawk_Eye_version_1.0_LP_recog\\Hawk_Eye_version_1.0_LP_recog\\Hawk_Eye_LP_recognition.py";

            //string fileName = @"D:\\gt.py";
            //string fileName = @"D:\\Hawk_Eye_version_1.0_LP_recog\\Hawk_Eye_version_1.0_LP_recog\\object_detection_yolo.py";
            string fileName = @"D:\\Hawk_Eye_version_1.0_LP_recog\\Hawk_Eye_version_1.0_LP_recog\\main_vehicle_to_LP.py";
            //string fileName = @"D:\\testWF.py";

            Process p = new Process();
            p.StartInfo = new ProcessStartInfo(@"D:\LOGICIELS\pythonn\WPy64-3740\python-3.7.4.amd64\python.exe")
            //p.StartInfo = new ProcessStartInfo(@"D:\testWF.py")
            {
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true,

            };
            //p.StartInfo.Arguments = "3";
            p.StartInfo.Arguments = string.Format("{0} --image={1}", fileName, image_path);
            
            //p.StartInfo.Arguments = string.Format("{0}", fileName);

            //MessageBox.Show(p.StartInfo.Arguments);
            p.Start();

            string output = p.StandardOutput.ReadToEnd();
            p.WaitForExit();
            
            string result = output.Substring(0, output.Length - 2);
            //output.CopyTo(0, result, 0, output.Length - 4);
            return (result);
            
            ////MessageBox.Show(output);
            
            //Console.WriteLine("mchet");
            //Console.ReadLine();
            //            Console.WriteLine(output);

            //Console.ReadLine();

        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
           
        }
    }
}
