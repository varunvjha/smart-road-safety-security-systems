const fs = require('fs')
const mongoose = require('mongoose')

require('dotenv').config()

var info = null
var a = []
var ob = {}
var scheme = []
var schemaObject = {}

fs.readFile('openalpr-group-results.csv', 'utf8' , (err, data) => {
  if (err) {
    console.error(err)
    return
  }
  info = data.split('\n')
  scheme = info[0].split(',')
  //console.log(info)

  for (i=1; i<info.length; i++){
      if (info[i]!=''){
        x = info[i].split(',')
        ob = {}
        for (j=0; j< x.length; j++){
            ob[scheme[j]] = x[j]
        }
        a.push(ob)
      }
  }
  //console.log(a)
  //console.log(scheme)
  
  for (i=0; i<scheme.length; i++){
      schemaObject[scheme[i]] = String
  }
  const formSchema = mongoose.Schema(schemaObject)

    listOfItems = mongoose.model('listOfItems', formSchema)

    mongoose.connect(process.env.mongoid, { useNewUrlParser: true }, () =>{
        console.log('DataBase Connected')
        // for (i=0; i<a.length; i++){
        //     // listOfItems.findOne({best_plate: a[i].best_plate}).then(
        //         listOfItems.findOne({best_plate: a[i].best_plate}, function (err, docs) { 
        //             if (err){ 
        //                 console.log(err) 
        //             } 
        //             else{ 
        //                 if (docs == null){
        //                     console.log(a[i].best_plate + 'does not exist\n')
        //                 }
        //                 else {
        //                     console.log(a[i].best_plate + ' exists\n')
        //                 }
        //             } 
        //         })
        // }

    
        for (i=0; i<a.length; i++) {
            listOfItems.find({best_plate: a[i].best_plate}, function (err, docs) { 
                if (err){ 
                    console.log(err) 
                } 
                else{ 
                    //console.log("Result : ", docs); 
                    if (docs == null){
                        console.log('Does Not Exist\n')
                    }
                    else {
                        console.log('Valid\n')
                    }
                } 
            })
        }


        // listOfItems.insertMany(a)
        // .then(ins =>{ 
        //     console.log(ins)  // Success 
        //     mongoose.connection.close()
        // }).catch(function(error){ 
        //     console.log(error)      // Failure 
        //     mongoose.connection.close()
        // })
    })
})