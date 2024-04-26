const express = require("express");
const { open } = require("sqlite");
const sqlite3 = require("sqlite3");
const path = require("path");
const bcrypt = require("bcrypt")

const databasePath = path.join(__dirname, "userData.db");
const app = express();

app.use(express.json());

let database = null;

const initializeDbAndServer = async () => {
  try {
    database = await open({
      filename: databasePath,
      driver: sqlite3.Database,
    });

    app.listen(3000, () =>
      console.log("Server Running at http://localhost:3000/")
    );
  } catch (error) {
    console.log(`DB Error: ${error.message}`);
    process.exit(1);
  }
};


initializeDbAndServer();

app.post("/register", async (request, response) => {

  const {username ,name, password, gender, location} = request.body

    const checkUserQuery = `select * from user where username = ${username};`;
    const hashedPassword = await bcrypt.hash(password, 10)

    const checkUser = await database.get(checkUserQuery);

    if (checkUser === undefined){
        if (password.length < 5 ) {
            response.status(400);
            response.send("Password is too short");
        }
        else{
            const postUserQuery = `insert into user (username ,name, password, gender, location )
            values ('${username}', '${name}', '${hashedPassword}', '${gender}', '${location}');`
            await database.run(postUserQuery)
            response.status(200);
            response.send("User created successfully")

        }
    }
    else{
        response.status(400)
        response.send("User already exists");
    }




}

app.post("/login", async (request, response) => {

  const {username , password} = request.body

    const checkUserQuery = `select * from user where username = ${username};`;

    const checkUser = await database.get(checkUserQuery);

    if (checkUser === undefined){
        response.status(400)
        response.send("Invalid User");
    }
    else{
        const checkPassword = await bcrypt.compare(password, checkUser.password);
        if(checkPassword){
            response.status(200);
            response.send("Login success!")

        }
        else{
            response.status(400);
            response.send("Invalid password")

        }
        
    }




}

app.put("/change-password", async (request, response) => {
    const {username , oldpassword, newPassword} = request.body
    const checkUserQuery = `select * from user where username = ${username};`;

    const checkUser = await database.get(checkUserQuery);
    const checkPassword = await bcrypt.compare(oldpassword, checkUser.password);

    if(checkPassword) {
        if (password.length < 5 ) {
            response.status(400);
            response.send("Password is too short");
        }
        else{
            const hashedPassword = await bcrypt.hash(newPassword, 10)
            const postUserQuery = `update  
            user set 
            password = '${hashedPassword}'
            where username = '${username}';`
            await database.run(postUserQuery)
            response.status(200);
            response.send("User created successfully")


    }
    else{
        response.status(400)
        response.send("Invalid current password")

    }


}
}



module.exports = app;