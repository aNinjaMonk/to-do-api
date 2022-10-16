const express=require('express');
const router=express.Router();
const { check ,validationResult}=require('express-validator');

const config=require('config');
const bcrypt=require('bcryptjs');
const jwt=require('jsonwebtoken');


const User =require('../../models/User');

// @route   POST api/registeruser
// @desc    Register user
// @access  Public

router.post('/',[ check('username','username required')
.not()
.isEmpty(),
    check('name','name required')
     .not()
     .isEmpty(),
    check('email','invalid email').isEmail(),
    check('password','minmum length is 6 character').isLength({ min:5})
  ],
async(req,res)=> {

   const errors=validationResult(req);
   if(!errors.isEmpty()){
       return res.status(400).json({ errors:errors.array()})
   }

   const { username,name, email, password }=req.body;

   try{

   // see if user exists
  let user=await User.findOne({ email });
   
   if(user){
   return  res.status(400).json({errors:[{ msg:'user already exists' }]});
   }


  
   user=new User({
    username,
     name,
     email,
     password
   });
   //encrypt password
     const salt=await bcrypt.genSalt(10);

     user.password=await bcrypt.hash(password,salt);

     await user.save();
   
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