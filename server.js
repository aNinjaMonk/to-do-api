const express=require("express");
const connectDB=require('./config/db');
const app=express();
//connect database
connectDB();

// init middleware
app.use(express.json());

app.get('/',(req,res)=>{
 res.send('API RUNNING');
})


app.use('/api/registeruser',require('./routes/api/registeruser'));
app.use('/api/login',require('./routes/api/login'));
app.use('/api/forgetusername',require('./routes/api/forgetusername'));
app.use('/api/addtodo',require('./routes/api/addtodo'));
app.use('/api/updatetodo',require('./routes/api/updatetodo'));
app.use('/api/listtodo',require('./routes/api/listtodo'));
app.use('/api/deletetodo',require('./routes/api/deletetodo'));
app.use('/api/analysetodo',require('./routes/api/analysetodo'));


const PORT=5000;

app.listen(PORT,()=>{
    console.log(`server started at ${PORT}`);
});
