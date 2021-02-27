const fs = require('fs')
const path = require('path');
const express = require('express');
const hbs = require('hbs');
const fileupload = require('express-fileupload');
// const { exec } = require("child_process");
const pycall = require('./utils/utils.js')

function catt(){
    try {
        const data = fs.readFileSync('./python/resources/classification_output/out.txt', 'utf8')
        console.log(data)
        return data;
      } catch (err) {
        console.error(err)
      }
}

function cattj(){
    try {
        const data = fs.readFileSync('./python/resources/classification_output/out.json', 'utf8')
        console.log(data)
        return data;
      } catch (err) {
        console.error(err)
      }
}

function trainable(){
    try {
        const data = fs.readFileSync('./python/resources/trainable.txt', 'utf8')
        console.log(data);        
        return data;
      } catch (err) {
        console.error(err)
      }
}


const app = express();
const port = process.env.PORT || 3000;

app.use(fileupload());

//define paths for express config
const publicDirectoryPath = path.join(__dirname,'/../public');
const viewsPath = path.join(__dirname,'../templates/views');
const partialsPath = path.join(__dirname,'../templates/partials');

//setup handlebars engine and views location
app.set('view engine','hbs');
app.set('views',viewsPath);
hbs.registerPartials(partialsPath);


//setup static directory to serve
app.use(express.static(publicDirectoryPath));


//global variables
var cat;
const hf = {
    title:"Automated Document detection",
    name: "Aravind, Ashik, Tilak, Amith"

};






app.get('/',(req,res)=>{
    const data = trainable();
    hf.data = data;
    res.render('index',hf);
});

app.get('/about',(req,res)=>{
    res.render('about',hf)
})

app.get('/help',(req,res)=>{
    res.render('help',hf)
})

app.get('/upload',(req,res)=>{
    
    res.render('upload',hf)
})

app.get('/train',(req,res)=>{
    res.render('train',hf)
})


app.get('/predict',async(req,res)=>{
     const category = await pycall('bash ./sh/p.sh');
     cat = category;
     res.render('upload',{
        title:"Automated Document detection",
        name: "Aravind, Ashik, Tilak, Amith",
        category : cat
        
     });
})

app.get('/uploadImage',async(req,res)=>{
    await pycall('bash ./sh/use_for_training.sh');
    res.send('ok');
    // console.log(category)
})


app.get('/uploadImageForNewClass',async(req,res)=>{
    await pycall('bash ./sh/create_new_doc.sh');
    hf.category =catt()
    res.render('upload',hf);
})

app.get('/pickCategory',async(req,res)=>{
    await pycall('bash ./sh/choose_doc_type.sh');
    hf.category = catt()
    
    res.render('upload',hf);
})

app.get('/ocr',async(req,res)=>{
    const status = await pycall('bash ./sh/ocr11.sh');
    if(status.toString() =='fail')
        // res.render('ocrout',hf);
        res.send('no template found data entry should be done manually')
        
    else{
        dat = cattj()
        datt = JSON.parse(dat) 
        res.send(datt)
    }
})

app.get('/trainable',async(req,res)=>{
    const status = await pycall('bash ./sh/train.sh');
    // console.log(status);
    res.render('train',hf);
    
})

app.get('*',(req,res) => {
    res.render('404',{
        title:'404',
        name:'Aravind,Ashik,Tilak,Amith',
        errorMessage:'Page not found :('
    })
})


app.post('/saveImage',(req,res)=>{

    if (!req.files){
        res.send("no file chosen for upload")
    }
    if(req.files){
        console.log(req.files);

        var file = req.files.file
        var filename = file.name;

        console.log(filename);

        

        file.mv(__dirname+'/../uploads/'+filename, function(err){
            if(err){
                res.send(err);
            }else{
                res.send('file uploaded');
            }
        })
    }
})




app.listen(port,()=>{
    console.log("listening on port: ",port);
})