var express       =  require('express');
var router        =  express.Router();

const User=require('../../models/User');

const jwt=require('jsonwebtoken');
const config=require('config');

var nodemailer    =  require('nodemailer');


router.post('/', async(req, res)=> {
   const email=req.body.email;
      
 let token1;
const payload={
      email:email
  }
  try {
    
 
  jwt.sign(
    payload,
    config.get('jwtSecret'),
    { expiresIn:3600000 },
    (err,token)=>{
      if(err) throw err;
      token1=token;
    }
    );
   
      
        const user=  User.findOne({ email: req.body.email });
            if (!user) {
              return res.json({msg:"Account with that email doesn't exists."});
            }
            var updatedUser = {
              resetPasswordToken : token1,
              resetPasswordExpires : Date.now() + 3600000
          }
    
          const res1123=
          await User.findOneAndUpdate(
              { email: req.body.email },
              { $set: updatedUser },
              { new: true }
            );
           
  
    
          var smtpTransport = nodemailer.createTransport({
            service: 'gmail',
            auth: {
              type: 'OAuth2',
              user: "email",
              pass: "your email password",
              clientId: "",
              clientSecret: ""
              ,
              refreshToken: ""
            }
            });
    
          var mailOptions = {
            to:       user.email,
            from:     'utkarshyadav9876@gmail.com',
            subject:  'Password Reset',
            text:     'You are receiving this because you have requested the reset of the password for your account.\n\n' +
              'Please click on the following link, or paste this into your browser to complete the process:\n\n' +
              'http://' + req.headers.host + '/users/reset-password/' + token1 + '\n\n' +
              'If you did not request this, please ignore this email and your password will remain unchanged.\n'
          }
       const res1= await  smtpTransport.sendMail(mailOptions );
        if(res1) {
            res.send('info', 'An e-mail has been sent to ' + user.email + ' with further instructions.');
         
          }
   
} catch (error) {
    console.error(error.message); 
       res.status(500).send('server error');
} 
  });
  
  router.get('/:token', async(req, res)=>{
    try {
  
 const user=await    User.findOne({
        resetPasswordToken: req.params.token, 
        resetPasswordExpires: {$gt: Date.now()}})
    if (!user) {
      res.send( 'Password reset token is either invalid or has expired');
      
    }
    

    res.send("token is valid to reset");
  }
    catch (error) {
      console.error(error.message);
         res.status(500).send('server error');
  }
  }
  
  );
  

  
  module.exports = router;