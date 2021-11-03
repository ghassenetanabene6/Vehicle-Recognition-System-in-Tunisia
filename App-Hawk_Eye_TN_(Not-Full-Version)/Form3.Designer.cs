namespace Hawk_Eye_App
{
    partial class Form3
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            this.btn_Camera = new System.Windows.Forms.Button();
            this.comboBox_device = new System.Windows.Forms.ComboBox();
            this.label1 = new System.Windows.Forms.Label();
            this.btn_recognition = new System.Windows.Forms.Button();
            this.btn_Confirm = new System.Windows.Forms.Button();
            this.btn_Deny = new System.Windows.Forms.Button();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            this.SuspendLayout();
            // 
            // pictureBox1
            // 
            this.pictureBox1.Location = new System.Drawing.Point(50, 12);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(511, 397);
            this.pictureBox1.TabIndex = 3;
            this.pictureBox1.TabStop = false;
            this.pictureBox1.Click += new System.EventHandler(this.pictureBox1_Click);
            // 
            // btn_Camera
            // 
            this.btn_Camera.Location = new System.Drawing.Point(609, 153);
            this.btn_Camera.Name = "btn_Camera";
            this.btn_Camera.Size = new System.Drawing.Size(121, 23);
            this.btn_Camera.TabIndex = 2;
            this.btn_Camera.Text = "Open the camera";
            this.btn_Camera.UseVisualStyleBackColor = true;
            this.btn_Camera.Click += new System.EventHandler(this.btn_Camera_Click);
            // 
            // comboBox_device
            // 
            this.comboBox_device.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.comboBox_device.FormattingEnabled = true;
            this.comboBox_device.Location = new System.Drawing.Point(609, 58);
            this.comboBox_device.Name = "comboBox_device";
            this.comboBox_device.Size = new System.Drawing.Size(121, 23);
            this.comboBox_device.TabIndex = 4;
            this.comboBox_device.SelectedIndexChanged += new System.EventHandler(this.comboBox_device_SelectedIndexChanged);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(607, 39);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(42, 15);
            this.label1.TabIndex = 5;
            this.label1.Text = "Device";
            // 
            // btn_recognition
            // 
            this.btn_recognition.Location = new System.Drawing.Point(609, 204);
            this.btn_recognition.Name = "btn_recognition";
            this.btn_recognition.Size = new System.Drawing.Size(121, 23);
            this.btn_recognition.TabIndex = 6;
            this.btn_recognition.Text = "Vehicle Recognition";
            this.btn_recognition.UseVisualStyleBackColor = true;
            this.btn_recognition.Click += new System.EventHandler(this.btn_recognition_Click);
            // 
            // btn_Confirm
            // 
            this.btn_Confirm.Location = new System.Drawing.Point(172, 421);
            this.btn_Confirm.Name = "btn_Confirm";
            this.btn_Confirm.Size = new System.Drawing.Size(75, 23);
            this.btn_Confirm.TabIndex = 7;
            this.btn_Confirm.Text = "Confirm";
            this.btn_Confirm.UseVisualStyleBackColor = true;
            this.btn_Confirm.Click += new System.EventHandler(this.btn_Confirm_Click);
            // 
            // btn_Deny
            // 
            this.btn_Deny.Location = new System.Drawing.Point(332, 421);
            this.btn_Deny.Name = "btn_Deny";
            this.btn_Deny.Size = new System.Drawing.Size(75, 23);
            this.btn_Deny.TabIndex = 8;
            this.btn_Deny.Text = "Deny";
            this.btn_Deny.UseVisualStyleBackColor = true;
            this.btn_Deny.Click += new System.EventHandler(this.btn_Deny_Click);
            // 
            // Form3
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(846, 450);
            this.Controls.Add(this.btn_Deny);
            this.Controls.Add(this.btn_Confirm);
            this.Controls.Add(this.btn_recognition);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.comboBox_device);
            this.Controls.Add(this.btn_Camera);
            this.Controls.Add(this.pictureBox1);
            this.Name = "Form3";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Camera";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.Form3_FormClosing);
            this.Load += new System.EventHandler(this.Form3_Load);
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        private System.Windows.Forms.Button btn_Camera;
        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.ComboBox comboBox_device;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button btn_recognition;
        private System.Windows.Forms.Button btn_Confirm;
        private System.Windows.Forms.Button btn_Deny;
    }
}