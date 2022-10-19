const express = require('express');
const mongoose=require('mongoose');
const router = express.Router();
const axios=require('axios');
const config=require('config');

const auth = require('../../middleware/auth');
const Todo = require('../../models/Todo');

router.get('/:id', auth, async (req, res) => {
    try {
      const todo = await Todo.findOne({user:req.user.id,_id:req.params.id});

 // Check for ObjectId format and post
 if (!mongoose.Types.ObjectId.isValid(req.params.id) || !todo) {
    return res.status(404).json({ msg: 'Todo not found' });
  }

const api_key=config.get("cloud_analysis_key");


const url=`https://language.googleapis.com/v1/documents:analyzeSentiment?key=${api_key}`;
const data={
  "document":{
    "type":"PLAIN_TEXT",
    "language": "EN",
    "content":todo.details
  },
  "encodingType":"UTF8"
};
 
  const response = await axios.post(url,
  JSON.stringify(data) 
    
    ,

  {
    method: 'POST', 
    headers: {
      'Content-Type': 'application/json'
      
    }
});

console.log(response.data.sentences[0].sentiment);
const analysedValue=response.data.sentences[0].sentiment;
  res.json({analysedValue}); 
 
  // var duedate=new Date(todo.duedate);
  // var todaydate=new Date();
  // if(todo.status==='done') 

  // else {
  //    if(duedate-todaydate<172800000)   //2 days
  //    res.json({msg:"Upcoming"});
  //    else if(duedate-todaydate<0) 
  //    res.json({msg:"Critical"});
  //    else  
  //    res.json({msg:"Relaxed"});
  //    } 
  //   //  if(todo.status==='working')
 

    } catch (err) {
      console.error(err);
      
      res.status(500).send('Server Error');
    }
  });
  module.exports=router;