const mongoose=require('mongoose');


const todoschema=new mongoose.Schema({
  title:{
    type:String,
    required:true
  }, 
 details:{
    type: String,
    required:true
},
status:{
    type: String,
    required:true
},
duedate:{
    type:Date,
    required:true

},
username:{
  type: String,
  required:true
},
user: {
  type:mongoose.Schema.Types.ObjectId,
  ref: 'users'
}
// can add isdeleted with default false if we don't want to remove data on deleting just set it to true and change all queries accordingly.
});


module.exports=Todo=mongoose.model('todo',todoschema);