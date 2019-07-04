/*
参数压暗范围：
(D10)Dark10：
idExps            = -2 ~ -1
factor            = 1
idgammaCorrection = 0.6 ~ 0.7

(D20)Dark20
idExps            = -3 ~ -2
factor            = 1
idgammaCorrection = 0.5 ~ 0.6

(D30)Dark30
idExps            = -0.5 ~ -0.4
factor            = 0.1
idgammaCorrection = 0.8 ~ 0.9

(GTD10)Ground Truth Dark10:
idExps            = -1 ~ 0
idgammaCorrection = 0.7 ~ 0.8

(GTD20)Ground Truth Dark10:
idExps            = -1 ~ 0
idgammaCorrection = 0.7 ~ 0.8
*/

//图片输入路径
var imgsPath = "E:\\Github\\test\\";
//图片保存路径
var imgsProcessedPath = "E:\\Github\\test_dark\\"

var postfix = "_D10.jpg"
var idExpsLowVal = -2
var factor = 1
var idgammaCorrectionLowVal = 0.6

while(app.documents.length)
{
    app.activeDocument.close()
}
var imgFolder = Folder(imgsPath)
var imgsList = imgFolder.getFiles()
for(var i = 0; i< imgsList.length; i++)
{
    if(imgsList[i] instanceof File)
    {
        var doc = open(imgsList[i])
        
        var addNum1 = Math.random();
        var addNum2 = Math.random();

        // =======================================================
        //饱和度操作，进行图像全局压暗
        var idExps = charIDToTypeID( "Exps" );
        var desc7 = new ActionDescriptor();
        var idpresetKind = stringIDToTypeID( "presetKind" );
        var idpresetKindType = stringIDToTypeID( "presetKindType" );
        var idpresetKindCustom = stringIDToTypeID( "presetKindCustom" );
        desc7.putEnumerated( idpresetKind, idpresetKindType, idpresetKindCustom );
        var idExps = charIDToTypeID( "Exps" );
        desc7.putDouble( idExps, idExpsLowVal + addNum1*factor);
        var idOfst = charIDToTypeID( "Ofst" );
        desc7.putDouble( idOfst, 0.0 );
        var idgammaCorrection = stringIDToTypeID( "gammaCorrection" );
        desc7.putDouble( idgammaCorrection, idgammaCorrectionLowVal + addNum2*0.1);
        executeAction( idExps, desc7, DialogModes.NO );

        //Save As
        var idsave = charIDToTypeID( "save" );
        var desc18 = new ActionDescriptor();
        var idAs = charIDToTypeID( "As  " );
        var desc19 = new ActionDescriptor();
        var idEQlt = charIDToTypeID( "EQlt" );
        desc19.putInteger( idEQlt, 12 );
        var idMttC = charIDToTypeID( "MttC" );
        var idMttC = charIDToTypeID( "MttC" );
        var idNone = charIDToTypeID( "None" );
        desc19.putEnumerated( idMttC, idMttC, idNone );
        var idJPEG = charIDToTypeID( "JPEG" );
        desc18.putObject( idAs, idJPEG, desc19 );
        var idIn = charIDToTypeID( "In  " );

        var curImgName = doc.name
        curImgName= curImgName.substr(0, curImgName.length - 4)
        outImgName = curImgName + postfix
        outImgName = imgsProcessedPath + outImgName
        desc18.putPath( idIn, new File( outImgName ) );
        var idDocI = charIDToTypeID( "DocI" );
        desc18.putInteger( idDocI, 195 );
        var idsaveStage = stringIDToTypeID( "saveStage" );
        var idsaveStageType = stringIDToTypeID( "saveStageType" );
        var idsaveSucceeded = stringIDToTypeID( "saveSucceeded" );
        desc18.putEnumerated( idsaveStage, idsaveStageType, idsaveSucceeded );
        executeAction( idsave, desc18, DialogModes.NO );

        app.activeDocument.close()
    }
}