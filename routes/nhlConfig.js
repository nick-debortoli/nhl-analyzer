const nhlConfig = {
    apiVersion: "v0.1",
    
    port: 8771,
    
    publicDirectory: "src",

    data: {
        debug: {
            detailed: true,
            info: true
        },

        type: "FIREBASE",  

        // database: {
        //     connectionLimit: 10,
        //     host: '127.0.0.1',
        //     port: 3306,
        //     user: 'root',
        //     password: 'mysql',
        //     databaseName: 'coda'
        // }
    }


}

module.exports = nhlConfig;