const express=require('express');
const router=express.Router();
const User=require('../../models/User');


const { oneOf,check ,validationResult}=require('express-validator');
const config=require('config');
const bcrypt=require('bcryptjs');
const jwt=require('jsonwebtoken');


// @route   POST api/login
// @desc    Authenticate user and get token
// @access  Public

router.post('/',[
  oneOf( 
  [
    check('email','invalid email').exists().isEmail(),
    check('username','usename required').exists().not().isEmpty(),
  ],
),
    // check('email','invalid email').isEmail(),
    check('password','password is required').exists()
  ],
async(req,res)=> {

   const errors=validationResult(req);
   if(!errors.isEmpty()){
       return res.status(400).json({ errors:errors.array()})
   }

   const { username,email, password }=req.body;

   try{
 let user;
   // see if user exists
   if(email)
  user=await User.findOne({ email });
  else   user=await User.findOne({ username });

   
   if(!user){
   return  res.status(400).json({errors:[{ msg:'user does not exists' }]});
   }

 
 const isMatch= await bcrypt.compare(password,user.password);
  if(!isMatch){
    return  res.status(400).json({errors:[{ msg:'incorrect password' }]});
  }
   
   //return jsonwebtoken
    

const payload={
  user:{
    id:user.id
  }
}

jwt.sign(
  payload,
  config.get('jwtSecret'),
  { expiresIn:3600000 },
  (err,token)=>{
    if(err) throw err;
    res.json({token});
  }
  );


   }
     catch(err){
       console.error(err.message);
       res.status(500).send('server error');
     }

  

});

module.exports=router;