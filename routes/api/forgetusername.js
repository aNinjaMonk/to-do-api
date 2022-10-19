const express=require('express');
const router=express.Router();
const {check,validationResult} =require('express-validator');

// @route   POST api/forhetusername
// @desc    forget username
// @access  Public

router.post(
"/",[
    check('email','invalid email').isEmail()
],async(req,res)=>{
    const errors=validationResult(req);
    if(!errors.isEmpty()){
        return res.status(400).json({ errors:errors.array()})
    }
const {email}=req.body;
try{

    // see if user exists
   let user=await User.findOne({ email }).select('username');
    
    if(!user){
    return  res.status(400).json({errors:[{ msg:'user does not exists' }]});
    }
 const username=user.username;
    res.json({username});

    }
      catch(err){
        console.error(err.message);
        res.status(500).send('server error');
      }
}
);


module.exports=router;