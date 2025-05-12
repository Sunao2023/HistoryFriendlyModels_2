package Chapter5;

import java.io.*;
import java.util.Random;

/*                                                                            *
 * The pharmaceutical industry and the role of demand: Simulation code        *
 * @author Christian Garavaglia & Michele Pezzoni                             *
 *                                                                            */


//BEFORE STARTING
//Parameters can be changed in the method getparams()
//You have to set the working folder in the method multisim() -> change dir =  "C:/your/favourite/folder/" with the path of the selected ;

//SUMMARY OF THE EXERCICES IN CHAPTER 5
//Imitation and patent protection
/*
We address this issue by analyzing two changes to the parameter settings.
First, we consider a simulation in which patent protection is granted
for 40 periods (as compared to 20 in the Standard Set). 
Next, as an extreme case, we investigate the effects of protection of only 1 period.
*/

//The properties of the innovative process
/*
We focus on two important dimensions of the innovative process. 
First, the richness of the opportunities for innovation. 
Second, the absence of cumulativeness in the innovative process 
(the fact that the knowledge accumulated in discovering and 
developing one drug does not confer significant advantages in the 
search for new products in different TCs and in the future). 

1) We run simulations with different probabilities of finding
a promising molecule in the search process, 
comparing the Standard Set (where the probability of finding
a “zero quality” molecule is z = 0.97) with a simulation in
which opportunities are richer (z = 0.90) and with one where
opportunities are poorer (z = 0.99).

2)Here, we focus on search efforts: in this formulation the 
probability of finding new promising molecules is now positively 
affected by previous (successful) research efforts.
To do so, the search function is modified so that in each period
the number of draws in the search space is an increasing
function of the number of drugs owned by a firm .
*/

//Market Fragmentation
/*
Thus, we explore the fragmentation issue by examining simulations
with different numbers of TCs (keeping the value of the aggregate
market unchanged ): from 200 TC in the Standard Set to 20 and 
(as an extreme case) to only 1. 
*/


//main class
public class C5Model{   
   //variable declaration
   static int    numOfFirm, numOfTC, endTime, searchFailure, 
                 mt, patentDuration, qualityMax, qualityCheck, numOfSubMKT,
                 numOfMol, patentWidth, lastImiTime, speedDevelopmentInno,
                 speedDevelopmentImi;
   static double totvalmkt, alfa_cumulativeness, alfa_cumulativeness_exp,
                 stab, costOfSearch, costOfResearchImi, costOfResearchInn, B,
                 drawCost, timeDevelop, interestRate,  TCPatientsCost,
                 TCPatientsRand, aValueCost, aValueRand, bValueCost, bValueRand,
                 cValueCost, cValueRand, qMolCost, qMolVar, accMkting,
                 qMolNull, quotaInvestedInSearch, erosion, eFailure, costProd,
                 omega, elasticity, outProLimit, minRD, addRD, minS, addS;  
   static Random r;
   static Random rand;
   static statistic ST;
   
   static TerapeuticCategory[] TC;
   static Firm[] F;
   static files FILE;
   
   static boolean draw1 = false;                                   
   String pathResults;
   
   public C5Model() {
        
        String mainPath = new File("").getAbsolutePath();
        String subPath  = this.getClass().getName().substring(0, this.getClass().getName().indexOf("."));
        pathResults     = mainPath+"/results/"+subPath;        
    }
   
   public static void getParams() {          
        //multiple simulations
        mt                   = 1000; 
        //Periods of simulation 
        endTime		     = 100;
        //Number of potential firms
        numOfFirm            = 50;
        //Probability of drawing a zero-quality molecule
        qMolNull             = 0.97;
        //Unit cost of search
        drawCost             = 20;
        //Unit cost of production
        costProd             = 1;
        //Unit cost of development of innovative drugs
        costOfResearchInn    = 60;
        //Unit cost of development of imitative drugs
        costOfResearchImi    = 20; 
        //Periods to develop a drug
        timeDevelop          = 24; 
        //Speed of devlopment of an innovative drug:
        //timeDevelop/speedDevelopmentInno=Periods to develop an innovative drug (8)
        speedDevelopmentInno =  3;
        //Speed of devlopment of an imitative drug:
        //timeDevelop/speedDevelopmentImi=Periods to develop an imitative drug (4)
        speedDevelopmentImi  =  6; 
        //Patent duration
        patentDuration       = 20; 
        //Patent width
        patentWidth          = 5;
        //Minimum quality threshold of the drugs to be sold on the market
        qualityCheck         = 30;
        //Interest rate 
        interestRate         = 0.08; 
        //Indicator of market leaders power in Equation 6
        omega                = 0.5;
        //Perceived price elasticity of demand in Equation 6
        elasticity           = 1.5;
       //Erosion rate of product image
        erosion              = 0.01;
        //Minimum market share threshold for survival of a firm in the market
        eFailure             = 0.004; 
        //Minimum market share threshold for survival of a product in the market
        outProLimit          = 0.05;
        //Periods without drawing a promising molecule after which an innovative firm exits
        searchFailure        = 7;

        //Therapeutic Classes, Molecules and Drugs Characteristics
        //Number of TCs
        numOfTC        = 200; 
        //Number of molecules in TC
        numOfMol       = 400; 
        //Number of potential patients in TC 
        //Mean of normal distribution of the number of patients per TC 
        TCPatientsCost = 600;
        //Standard deviation of normal distribution of the number of patients per TC
        TCPatientsRand = 200; 
        //Number of groups of patients in TC h that might buy drug j
        numOfSubMKT    = 4;

        //Economic value of a TC h
        //Weight of product quality for TC h in Equation 9
        aValueCost = 0.5;
        aValueRand = 0.1;
        //Weight of inverse of price for TC h in Equation 9
        bValueCost = 0.15;
        bValueRand = 0.05;
        //Weight of product image for TC h in Equation 9
        cValueCost = 0.35;
        cValueRand = 0.05; 
       //Mean of normal distribution of positive quality molecules
        qMolCost   = 30;                
       //Standard deviation of normal distribution of positive quality molecules
        qMolVar    = 20;

       //Firm characteristics
       //Fraction of budget invested in R&D activities by firm f
       minRD = 0.25;
       addRD = 0.5;
       //Fraction of budget invested in search activities by firm f
        minS = 0.1;
        addS = 0.05;
       //Initial budget of a potential firm
        B    = 4500;
        
       //OTHER PARAMETERS             
	costOfSearch          = 0;
        accMkting             = 30;
        qualityMax            = 90;                       
        quotaInvestedInSearch = 0.1;               
        alfa_cumulativeness   = 1; //draw1
             
        //SWITCHES                           
        //probability of finding new promising molecules is positively 
        //affected by previous (successful) research efforts when dwaw1=true                                          
        draw1 = false; //numberDraw = (int) (Math.round((searchExpenditure/C5Model.drawCost))+(alfa_cum*prod));                          
      }

/*loop of multi / single simulations*/ 
  public void makeMultipleSimulation() {       
        //create arrays to store reults and statistics
        getParams();
        FILE = new files();
        ST = new statistic();
        ST.createArray(endTime, numOfTC,numOfFirm);
        ST.initMulti(endTime, numOfTC);
	//start multi simulations
        int tt = 1;
        int assignedseed = 1;
        while (tt <= mt) {
            //select seed
            r = new Random();
            r.setSeed(assignedseed);        
            getParams();
            //create arrays of firms and TC
            TC = new TerapeuticCategory[numOfTC];
	    F = new Firm[numOfFirm];
            ST.initValue(endTime,numOfTC,numOfFirm);	    
            initTC();
	    initFirm();
            //start of single simulation
            for(int time = 1; time <= endTime; time++ ){
                    entry(numOfFirm,time);                    
		    molValue(time);                    
		    methodOfSearch(time);
                    checkMol(time);
		    reasearchActivity(time);
                    mkting(time);
		    calcShare(time);
		    calcProfit(time);
		    ST.statistics(time, mt, numOfTC, numOfMol, numOfFirm);
                    exitRule(time); 
		}
            //end single simulation
            System.out.print(tt+"\n");
                  tt++;
                  //change seed for the next single simulation
                  assignedseed++;            
	}
        //end multi simualtion
        
        //record statistics     
    	FILE.initFiles(pathResults);
        ST.reportXls(endTime, numOfFirm, numOfTC);
        FILE.closeFiles();	
        System.out.println("end of sim");               
}
  
public void makeSingleSimulation() {       
        //create arrays to store reults and statistics
        getParams();
        FILE = new files();
        ST = new statistic();
        ST.createArray(endTime, numOfTC,numOfFirm);
        ST.initMulti(endTime, numOfTC);
	int assignedseed = 1;
        //select seed
        r = new Random();
        r.setSeed(assignedseed);        
        getParams();
        //create arrays of firms and TC
        TC = new TerapeuticCategory[numOfTC];
	F = new Firm[numOfFirm];
        ST.initValue(endTime,numOfTC,numOfFirm);	    
        initTC();
	initFirm();
        //start of single simulation
        for(int time = 1; time <= endTime; time++ ){
            entry(numOfFirm,time);                    
	    molValue(time);                    
	    methodOfSearch(time);
            checkMol(time);
            reasearchActivity(time);
            mkting(time);
            calcShare(time);
            calcProfit(time);
            ST.statistics(time, mt, numOfTC, numOfMol, numOfFirm);
            exitRule(time); 
        }
        //end single simulation
        //record statistics     
    	FILE.initFiles(pathResults);
        ST.reportXls(endTime, numOfFirm, numOfTC);
        FILE.closeFiles();	
        System.out.println("end of sim");               
}  

//It defines the characteristics of the TC: exponents in Equation 9
   public static void initTC(){       
        for(int i=0;i<numOfTC;i++) {
            double val = r.nextGaussian()*TCPatientsRand+TCPatientsCost;
            //random distribution of values larger than zero
            if(val<0) val=0;
	    TC[i] = new TerapeuticCategory(i,val,// TC value STD
                                       (aValueCost-aValueRand+(2*C5Model.r.nextDouble()*aValueRand)),	// a
				       (bValueCost-bValueRand+(2*C5Model.r.nextDouble()*bValueRand)),	// b
				       (cValueCost-cValueRand+(2*C5Model.r.nextDouble()*cValueRand)),	// c
				       endTime);
            TC[i].setSubMKTValue();
        }
   }

   public static void initFirm(){
       double specificRateInvSearch;
       boolean innovatorFirm = true;
       for(int i=0; i<numOfFirm; i++){
           //proportion of R&D budget invested in search
           specificRateInvSearch = quotaInvestedInSearch + (C5Model.r.nextDouble()*minS - addS);
           double x=C5Model.r.nextDouble();
           //proportion of budget invested in marketing
           double PropensionToMkting=(minRD+addRD*x);
           //PropensionToMkting and specificRateInvSearch are the parameters used in the equations 1.a, 1.b, and 1.c
           F[i] = new Firm(
                        //initial budget
                        (double) B,                 
                        //proportion of budget invested in marketing                
                        PropensionToMkting,
                        //proportion of budget invested in R&D activities
                        (1 - PropensionToMkting), 
                        //propension of R&D budget devoted to seacrh activities
                        specificRateInvSearch,
                        //total number of TC in the environment. It is used to define firm's vector size
                        (int) numOfTC, 
                        //it defines if the firm is currently classified as an innovator or an imitator according to the number of innovative / imitative products it has (in the beginning of the simulation all firms are defined innovator)
                        innovatorFirm,
                        //It defines the firm's propensity to be innovative or imitative
                        x);
       }
   }

//Sets all the firms alive in teh first period of the simulation
   public static void entry(int nfirm, int t){
       if(t==1)
           for(int i=0; i<nfirm; i++){
               C5Model.F[i].alive=true;
           }
   }

   //set the molecule values for each TC    
   public static void molValue(int t){
       if (t==1) {
           for(int i=0; i<numOfTC;i++){
               for(int ii=0; ii<=numOfMol; ii++){
                   double random = r.nextDouble()*1;
                   if (random > qMolNull){
                       TC[i].Mol[ii].q = (int) (Math.round(r.nextGaussian()*qMolVar)+qMolCost);
                   }
                   else TC[i].Mol[ii].q = 0;
               }
               TC[i].calcQMinInSMKT();
           }
       }
   }
   
   /*Firms are heterogeneous in two respects: they can behave as
   innovators or imitators. Innovators look for new molecules 
   by randomly screening the possible molecules and incur a search cost. 
   Imitators select among the molecules whose patent has expired,
   thus avoiding the cost of search*/
   public static void methodOfSearch (int t) {
       int initFirm=0;
       initFirm=(int) (C5Model.r.nextDouble()*C5Model.numOfFirm);
       //the two for cycles and the avriable "initFirm" avoid that firms are treated always in the same order
       for (int i=initFirm; i<numOfFirm; i++)
           if((F[i].alive==true)){
               //"chooseImIn()" defines if the firm is imitator or innovator according to its propensity
               F[i].innovatort=F[i].chooseImIn();
               //calculates the number of products
               F[i].clacImiInno(t);
               //selects "inno" behaviour if the firm is an innovator or 
               //if there are no products to imitate 
               //"selectionImitTaBestEarnings(i,t) == -1)", otherwise it selected "imi" behaviour
               if(F[i].innovatort == true || (F[i].innovatort == false && selectionImitTCBestEarnings(i,t) == -1)){
                   //sets the budget available for search / development of current products and total budget
                   //see equation 2 in the chapter
                   F[i].search(t, "inno", C5Model.drawCost);   
                   //It does search activity and records the drawn molecules in "onProInno"
                   F[i].SearchAction.doSearch(t,F[i].totProd);
               }
               else F[i].search(t, "imi", 0);
               searchActivity(t, i);
           }
       //the commet of the previous for cycle apply to this cycle
       for (int i=0; i<initFirm; i++) {
           if((F[i].alive==true)){
               F[i].innovatort=F[i].chooseImIn();
               F[i].clacImiInno(t);
               if(F[i].innovatort == true || (F[i].innovatort == false && selectionImitTCBestEarnings(i,t) == -1)){  
                   F[i].search(t, "inno", C5Model.drawCost);
                   F[i].SearchAction.doSearch(t,F[i].totProd);
               }
               else F[i].search(t, "imi", 0);
               searchActivity(t, i);
           }
       }
   }

   //The firms selects to imitate an existing product with the patent expired or to innovate
   //the choice bases on the availability of a product to imitate "controlImitTa" and on the propensity of the firm to one of the two activities "F[f].innovatort"
   public static void searchActivity(int time, int f){
       int controlImitTa;
       controlImitTa = selectionImitTCBestEarnings(f,time);
       if(controlImitTa == -1) {
           innovationBehaviour(time, f);
           F[f].nowInno=true;
       }
       else {
           if(F[f].innovatort == false) {
               imitationBehaviour(time, f);
               F[f].nowInno=false;
           }
           else {
               innovationBehaviour(time, f);
               F[f].nowInno=true;
           }
       }
   }

   //This method assigns a value to the TCs where the promosing molecules (stored in onProInno) are located and patent the ones which are not patented yet
   public static void innovationBehaviour(int t, int firm){
       //The firms assign a value to the molecule that is located in the TC according to the average earnings of the other existing products in the same TC
       for(int pr=0; pr<F[firm].onProInno.value.length; pr++){
           //the methos "meanMup(..,"earnings")" provides the average earnings of the products already sold in the TC
           F[firm].onProInno.value[pr]=(int) meanMup(F[firm].onProInno.MemOfTC[pr],t,elasticity,"earnings");
           F[firm].onProInno.weight[pr]=C5Model.speedDevelopmentInno;
       }
       for(int n=0; n<F[firm].SearchAction.numberDraw; n++) {
           if((TC[F[firm].SearchAction.portfolioTC[n]].Mol[F[firm].SearchAction.portfolioMol[n]].nowFree == false)&&
                   (TC[F[firm].SearchAction.portfolioTC[n]].Mol[F[firm].SearchAction.portfolioMol[n]].patent == false)&&
                   (TC[F[firm].SearchAction.portfolioTC[n]].Mol[F[firm].SearchAction.portfolioMol[n]].q>0)){
               //The firm patents the molecule if it is promising q>0 and it is not patented yet
               TC[F[firm].SearchAction.portfolioTC[n]].patent(F[firm].SearchAction.portfolioMol[n], t,firm);
           }
       }
   }

   //This method assigns a value to the TCs where the promosing molecules (stored in onProImi) are located
   public static void imitationBehaviour(int t, int firm) { 
       F[firm].onProImi.recordMemoryImi();
       for(int pr=0; pr<F[firm].onProImi.value.length; pr++){
           //the methos "meanMup(..,"earnings")" provides the average earnings of the products already sold in the TC
           F[firm].onProImi.value[pr]=(int) (meanMup(F[firm].onProImi.MemOfTC[pr],t,elasticity,"earnings"));
           F[firm].onProImi.weight[pr]=C5Model.speedDevelopmentImi;
       }
   }

   //Check if the patent is still active
   public static void checkMol(int t){
       for(int i=0;i<numOfTC;i++) {
           TC[i].patentTimeControl(t, patentDuration);
           TC[i].onTaRes=0;
       }
   }
   
   //This method defines the development activity of the firms
   public static void reasearchActivity(int t){ 
       for(int i = 0; i<numOfFirm; i++){
           if(F[i].alive==true){
               F[i].totcostt=0;
               //indentifies which molecules have to be developed according to the available budget and the value of the TC (innovative projects)
               if((F[i].alive == true) && F[i].nowInno == true){
                   F[i].mProj.in(F[i].onProInno.weight, F[i].onProInno.value, F[i].numprojects(F[i].nowInno, C5Model.timeDevelop) ,i,t);
               }
               //indentifies which molecules have to be developed according to the available budget and the value of the TC (imitative projects)
               if((F[i].alive == true) && F[i].nowInno == false){
                   F[i].mProj.in(F[i].onProImi.weight, F[i].onProImi.value, F[i].numprojects(F[i].nowInno, C5Model.timeDevelop),i,t);
               }
               //it updates the development status of the projects/products and the budget
               F[i].research(t);
               //it generates a new innovative product when the development phase is over
               for(int o=0; o<F[i].onProInno.MemOfTC.length; o++){
                   if(F[i].onProInno.state[o]>=C5Model.timeDevelop){
                       if(TC[F[i].onProInno.MemOfTC[o]].Mol[F[i].onProInno.MemOfMol[o]].q >= C5Model.qualityCheck
                               && F[i].onProInno.on[o]==1 && F[i].onProInno.done[o]==false){
                           //It generates a new product
                           F[i].newProduct(TC[F[i].onProInno.MemOfTC[o]].Mol[F[i].onProInno.MemOfMol[o]].q,
                                   //budget set aside for the launch of the product
                                   F[i].onProInno.mktingVet[o],
                                   meanMup(F[i].onProInno.MemOfTC[o],t,elasticity,"mup"),
                                   F[i].onProInno.MemOfTC[o],
                                   F[i].onProInno.MemOfMol[o],
                                   TC[F[i].onProInno.MemOfTC[o]].Mol[F[i].onProInno.MemOfMol[o]].nowFree,
                                   TC[F[i].onProInno.MemOfTC[o]].Mol[F[i].onProInno.MemOfMol[o]].focal,
                                   t, 1+t-F[i].onProInno.timeSv[o]);
                       }
                       F[i].onProInno.done[o]=true;
                   }
               }
               //it generates a new imitative product when the development phase is over
               for(int o=0; o<F[i].onProImi.MemOfTC.length; o++){
                   if(F[i].onProImi.state[o]>=C5Model.timeDevelop){
                       if(TC[F[i].onProImi.MemOfTC[o]].Mol[F[i].onProImi.MemOfMol[o]].q >= C5Model.qualityCheck
                               && F[i].onProImi.on[o]==1 && F[i].onProImi.done[o]==false){
                           //new product for the focal firm
                           F[i].newProduct(TC[F[i].onProImi.MemOfTC[o]].Mol[F[i].onProImi.MemOfMol[o]].q,
                                   F[i].onProImi.mktingVet[o],
                                   //the method "meanMup(..,"mup")" provides a price of entry of the product that is coherent with the prices of the other products in the TC
                                   meanMup(F[i].onProImi.MemOfTC[o],t,elasticity,"mup"),
                                   F[i].onProImi.MemOfTC[o], F[i].onProImi.MemOfMol[o],
                                   TC[F[i].onProImi.MemOfTC[o]].Mol[F[i].onProImi.MemOfMol[o]].nowFree,
                                   TC[F[i].onProImi.MemOfTC[o]].Mol[F[i].onProImi.MemOfMol[o]].focal,
                                   t, (1+t-F[i].onProImi.timeSv[o]));
                       }
                       F[i].onProImi.done[o]=true;
                   }
               }
               //assignes marketing budget to each product according to the state of development
               F[i].ProjMkting();
           }
       }
   }

  
   public static int selectionImitTCBestEarnings(int firm, int t) {
       int selectedTC = -1;
       double gain = 0;
       int best = -1;
       double[] prodTa, Profit;
       prodTa = new double[C5Model.numOfTC];
       Profit = new double[C5Model.numOfTC];
        
       for(int ii=0; ii<C5Model.numOfFirm; ii++) if((C5Model.F[ii].alive == true)){
           for(int iii=1; iii<=C5Model.F[ii].numOfProducts; iii++){
               if(F[ii].Prod[iii].out==false){
                   Profit[C5Model.F[ii].Prod[iii].TC]+=C5Model.F[ii].Prod[iii].historyEarnings[t-1];
                   prodTa[C5Model.F[ii].Prod[iii].TC]++;
               }
           }
       }
       
       for(int ii=0; ii<C5Model.numOfFirm; ii++) if((C5Model.F[ii].alive == true) && (C5Model.F[ii].numOfProducts>0)){
           for(int iii=1; iii<=C5Model.F[ii].numOfProducts; iii++)
               if(C5Model.TC[C5Model.F[ii].Prod[iii].TC].Mol[C5Model.F[ii].Prod[iii].mol].nowFree == true
                       && F[ii].Prod[iii].out==false
                       && (Profit[C5Model.F[ii].Prod[iii].TC])>gain) {
                   best=C5Model.F[ii].Prod[iii].TC;
                   gain=(Profit[C5Model.F[ii].Prod[iii].TC]);
               }
       }
       selectedTC=best;
       return selectedTC;
   }

  
    //calculates the market shares of each product
    //The method takes into account that each TC is devided in 4 submarkets and 
    //that the products competing in each submarket are the ones which overcome the quality threshold specific of each submarket
    //see equation 10 and 11 in chapter 5
   public static void calcShare(int time){
       for(int i=0; i<numOfTC; i++){
           TC[i].storePos = 0;
           for(int ii=0; ii<numOfSubMKT; ii++){
               TC[i].sMKT[ii].storePos = 0;
           }
       }
       
       for(int f=0; f<numOfFirm; f++) if(F[f].alive == true) {
           for(int p=1; p<=F[f].numOfProducts; p++){
               for(int s=0; s<numOfSubMKT; s++){
                   if((F[f].Prod[p].qp > TC[F[f].Prod[p].TC].sMKT[s].qMinReq) && F[f].Prod[p].out==false) {
                       F[f].Prod[p].subMKT = s;
                   }
               }
           }
       }

       for(int f=0; f<numOfFirm; f++) if(F[f].alive == true) {
           for(int p=1; p<=F[f].numOfProducts; p++){
               for(int t=0; t<numOfTC; t++){
                   for(int s=0; s<numOfSubMKT; s++){
                       if(F[f].Prod[p].TC == t && F[f].Prod[p].subMKT >= s && F[f].Prod[p].out==false){
                           //"probOfSell" calculates an utility value of the product as a function of its quality, price and marketing investment
                           F[f].Prod[p].probOfSell(time,f);
                           //calculates the sum of the utility values of all the products sold in each submarket
                           TC[F[f].Prod[p].TC].sMKT[s].storePos += F[f].Prod[p].pos;
                       }
                   }
               }
           }
       }
       
       for(int f=0; f<numOfFirm; f++) if(F[f].alive == true) {
           for(int p=1; p<=F[f].numOfProducts; p++){
               F[f].Prod[p].numPatients = 0;
               for(int t=0; t<numOfTC; t++){
                   for(int s=0; s<numOfSubMKT; s++){
                       if(F[f].Prod[p].TC == t && F[f].Prod[p].subMKT >= s && F[f].Prod[p].out==false){
                           double swap=0;
                           if(TC[F[f].Prod[p].TC].sMKT[s].storePos >0) {
                               swap = F[f].Prod[p].pos / TC[F[f].Prod[p].TC].sMKT[s].storePos;
                           }
                           if(TC[F[f].Prod[p].TC].sMKT[s].storePos <=0) swap = 0;                                                 
                           //records the total number of patients reached by the product in the TC summing the patients reached in each submarket. This code is the base for equation 10 and equation 11
                           F[f].Prod[p].numPatients    += swap*TC[t].sMKT[s].valueMKT;
                           //records the patients reached in each submarket
                           F[f].Prod[p].subMKTvalue[s]  = swap*TC[t].sMKT[s].valueMKT;
                       }
                   }
               }
           }
       }
   }

  public static void calcProfit(int time){
      double[] reachedPatients = new double[numOfTC];
      double[] reachedProfit = new double[numOfTC];
      
      //calculates the sum the patents reached by the firm in each TC
      for(int i=0; i< numOfFirm; i++) if(F[i].alive == true){
          F[i].totalReachedPatients=0;
          for(int p=1; p<=F[i].numOfProducts; p++){
              if(F[i].Prod[p].out==false){                  
                  reachedPatients[F[i].Prod[p].TC]+=F[i].Prod[p].numPatients;
                  F[i].totalReachedPatients+=F[i].Prod[p].numPatients;
              }
          }
      }
      
      //calculates the share of patients reached per TC
      for(int i=0; i< numOfFirm; i++) if(F[i].alive == true){
          for(int tas=0; tas<numOfTC;tas++){                
              F[i].shTC[tas] = 0;
          }
          F[i].totProfit = 0;
          for(int p=1; p<=F[i].numOfProducts; p++){
              if(F[i].Prod[p].out==false){
                  F[i].Prod[p].share = F[i].Prod[p].numPatients/reachedPatients[F[i].Prod[p].TC];
                  F[i].shTC[F[i].Prod[p].TC]+=F[i].Prod[p].share;
              }
          }
      }
      //update the mark-up of each product. The markup might change according to the entry / exit of new firms in the TC
      calcMup(numOfFirm, numOfTC, F, FILE, TC, time, omega, elasticity); 
      
      //calculate firm's profit
      for(int i=0; i< numOfFirm; i++) if(F[i].alive == true){
          for(int p=1; p<=F[i].numOfProducts; p++){
              if(F[i].Prod[p].out==false){
                  //It calculates the profits according to the cost of production and the markup value
                  F[i].Prod[p].historyPatients[time]=F[i].Prod[p].numPatients;
                  //see equation 12 in chapter 5. (P-cost)*q= (cost*(1+markup)-cost)*q=cost*markup*q
                  F[i].totProfit += (costProd*F[i].Prod[p].mup)*F[i].Prod[p].numPatients;
                  F[i].Prod[p].historyEarnings[time] = (costProd*F[i].Prod[p].mup)*F[i].Prod[p].numPatients;                       
                  reachedProfit[F[i].Prod[p].TC]+=((costProd*F[i].Prod[p].mup)*F[i].Prod[p].numPatients);
              }
          }
          //add the profites to the firm budget                    
          F[i].accounting();
      }
      //claulate share of the produc
      for(int i=0; i< numOfFirm; i++) if(F[i].alive == true){ 
          for(int p=1; p<=F[i].numOfProducts; p++){
              if(F[i].Prod[p].out==false){
                  F[i].Prod[p].shareP = (F[i].Prod[p].historyEarnings[time]/reachedProfit[F[i].Prod[p].TC]);
              }
          }
      }
  }
 
 //calculate the mark-up of the product
 public static void calcMup(int numOfFirm, int numOfTa, Firm[] firm, files FiLe, TerapeuticCategory Ta[], int time, double eta, double elasticity){
     for(int f=0; f<numOfFirm; f++){
         for(int p=1; p<=firm[f].numOfProducts; p++){
             if(F[f].Prod[p].out==false) 
                 //see equation 6 in chapter 5
                 C5Model.F[f].Prod[p].mup = 
                         ( ( (1-eta)*(C5Model.F[f].Prod[p].mup) ) + 
                         ( (eta)*(C5Model.F[f].shTC[C5Model.F[f].Prod[p].TC]/(elasticity-C5Model.F[f].shTC[C5Model.F[f].Prod[p].TC])))); 
         }
     }
 }

 public static double meanMup(int Area,int t, double elasticity, String st){         
     double mean=0;
     double count=0;
     double AreaMupMean = 0;
     double meanEarnings = 0;
     double meanProfit = 0;
     
     for(int ii=0; ii<C5Model.numOfFirm; ii++) if((C5Model.F[ii].alive == true) && (C5Model.F[ii].numOfProducts>0)){            
         for(int iii=1; iii<=C5Model.F[ii].numOfProducts; iii++){
             if(Area==C5Model.F[ii].Prod[iii].TC && F[ii].Prod[iii].out==false) {
                 mean+=C5Model.F[ii].Prod[iii].mup;
                 count++;
                 meanEarnings+=(C5Model.F[ii].Prod[iii].historyEarnings[t-1]);
                 meanProfit+=C5Model.F[ii].Prod[iii].historyEarnings[t-1];
             }
         }
     }
     
     if(meanEarnings>0)
         meanEarnings=(meanEarnings);
     else              
         //if the TC is not yet explored by other firms, the firms enters as monopolist,.i.e. the share at the numerator in the formula below equals to one
         meanEarnings=(C5Model.TC[Area].value*(1/(elasticity-1))*C5Model.costProd);
     
     if(meanProfit>0)
         meanProfit=meanProfit;
     else
         //if the TC is not yet explored by other firms, the firms enters as monopolist,.i.e. the share at the numerator in the formula below equals to one
         meanProfit=(C5Model.TC[Area].value*(1/(elasticity-1))*C5Model.costProd);
     if(mean>0)
         AreaMupMean=(mean/count);
     else
         AreaMupMean=((1/(elasticity-1)));
     //the method returns the average earning in the TC or the average muarkup in the TC
     if(st.equals("earnings")) return  meanEarnings;
     else return AreaMupMean;
 }


 //it defines the budget of the firm devoted to marketing and calculates the interests
 public static void mkting(int time){
     for(int i=0; i< numOfFirm; i++) if(F[i].alive == true){
         F[i].mkting();
         F[i].interest(interestRate);
     }
 }


 //it defines the exit rules of the firm and of the products. 
 //the products exit the market with the method "productsOut"
 //the firms exit the market with the method "failure"
 public static void exitRule(int time) {
     for(int firm=0; firm<C5Model.numOfFirm; firm++) {
         C5Model.F[firm].productsOut(C5Model.outProLimit);            
         if(C5Model.F[firm].alive == true && C5Model.F[firm].numOfProducts>0){
             double shareFirmTime = C5Model.F[firm].totShare[time];
             double E;
             double Efailure = C5Model.eFailure; 
             E=shareFirmTime;
             if(E<Efailure) C5Model.F[firm].failure();
         }
     }
 }

}

class Molecule{
    int id, 
        //firm that patented the molecule
        patentBy=-1, 
        //quality of the molecule
        q, 
        //time when the molecule has been patented    
        patentTime, 
        //identifies the molecule that is patented. N.B. similar variants of the focal molecule are patented. For these variants focal equals 0
        focal=0, 
        //A product based on this modlecule has been developed    
        productsOn=0, 
        //counts how many firms are doing research on the same molecule. It may happend that more than one firm is doing research 
        // on the same molecule when imitating an existing product.
        onMolRes=0;
    boolean 
            //if the molecule is patented
            patent, 
            //if the patent expired
            nowFree;

    Molecule (int ID, int Q){        
	id = ID;
	q  = Q;
	patent  = false;
	nowFree = false;
    }
}

class TerapeuticCategory {  

    int id, 
        //counts the number of products in the TC
        prodInTC = 0;
    double 
            //Count the number of patientes in the TC
            value, 
            //represents the importance of the quality of the drugs
            a, 
            //represents the importance of the price of the drugs
            b, 
            //represents the importance of the marking investment of the drug
            c, 
            //the value of the utility of the drugs
            storePos,  
            //count of frms doing development activities in the TC
            onTaRes;
    
    subMKT[] sMKT = new subMKT[C5Model.numOfSubMKT];
    Molecule[] Mol = new Molecule[C5Model.numOfMol + 1];

    //TC statistics
    double[] dim = new double[C5Model.endTime + 1];
    double[] pat = new double[C5Model.endTime + 1]; 
    double[] Herfindahl, Herfindahl1;
    double[] shareSum;
    double[] shareLeader; 
    double[] shareInnoLeader;
    int[] inFirm;
    int[] inProduct;
    int[] inProductOnlyInno;
    double[] existingQ;   
    double[] existingQall;

    TerapeuticCategory(int ID, double VAL, double A, double B, double C, int T) {            

        id = ID;
        value = VAL;     
        a = A;
        b = B;
        c = C;

        for (int i = 0; i < C5Model.numOfSubMKT; i++) {
            sMKT[i] = new subMKT();
        }

        for (int i = 0; i <= C5Model.numOfMol; i++) {
            Mol[i] = new Molecule(i, 0);
        }

        Herfindahl = new double[T + 1];
        Herfindahl1 = new double[T + 1];
        shareSum = new double[T + 1];
        shareLeader = new double[T + 1];
        shareInnoLeader = new double[T + 1];
        inFirm = new int[T + 1];
        inProduct = new int[T + 1];
        inProductOnlyInno = new int[T + 1];
        existingQ = new double[T + 1];
        existingQall = new double[T + 1];

        for (int t = 0; t <= T; t++) {
            Herfindahl[t] = 0;
            Herfindahl1[t] = 0;
            shareSum[t] = 0;
            shareLeader[t] = 0;
            shareInnoLeader[t] = 0;
            inFirm[t] = 0;
            inProduct[t] = 0;
            inProductOnlyInno[t] = 0;
            existingQ[t] = 0;
            existingQall[t] = 0;
        }
    }

//it checks when patents expire
    public void patentTimeControl(int t, int pd) {        
        for (int i = 0; i <= C5Model.numOfMol; i++) {
            this.Mol[i].onMolRes = 0;
            if ((t - Mol[i].patentTime >= pd) && (Mol[i].patent == true)) {
                unpatent(i);
            }
        }
    }

//THIS METHOD DEFINES THE "VERTICAL" AND "HORIZONTAL" PROTECTION TO PATENTED MOLECULES.
    public void patent(int id, int t, int f) {        
        if ((id >= C5Model.patentWidth) && (id <= (C5Model.numOfMol - C5Model.patentWidth))) {
            if (Mol[id].patent == false) {
                Mol[id].patentBy = f;
            }
            for (int i = id - C5Model.patentWidth; i <= id + C5Model.patentWidth; i++) {
                if (Mol[i].patent == false) {
                    Mol[i].patent = true;
                    Mol[i].patentTime = t;
                    Mol[id].focal = 2; 
                }
            }
        }
        if (id < C5Model.patentWidth) {
            if (Mol[id].patent == false) {
                Mol[id].patentBy = f;
            }
            for (int i = 0; i <= id + C5Model.patentWidth; i++) {
                if (Mol[i].patent == false) {
                    Mol[i].patent = true;
                    Mol[i].patentTime = t;
                    Mol[id].focal = 2; 
                }
            }
        }
        if (id > (C5Model.numOfMol - C5Model.patentWidth)) {
            if (Mol[id].patent == false) {
                Mol[id].patentBy = f;
            }
            for (int i = id - C5Model.patentWidth; i <= C5Model.numOfMol; i++) {
                if (Mol[i].patent == false) {
                    Mol[i].patent = true;
                    Mol[i].patentTime = t;
                    Mol[id].focal = 2; 
                }
            }
        }

    }

//this method unpatents the molecules
    public void unpatent(int ii) { 
        Mol[ii].patent = false;
        if (Mol[ii].focal == 2) {
            Mol[ii].nowFree = true;
        }
    }

//submarket within TC
    public class subMKT {
        double valueMKT;
        int qMinReq;
        int qMaxInTa;
        
        public subMKT() {
        }
        
        public double storePos;

    }

 
 //claculate the submarket value
    public void setSubMKTValue() { 
        double subValue = value / C5Model.numOfSubMKT;
        for (int i = 0; i < C5Model.numOfSubMKT; i++) {
            sMKT[i].valueMKT = subValue;
        }
    }

//calculate the minimum quality needed by the drug to be sold in each sub-market
   public void calcQMinInSMKT() { 
            int bestQ = 0;
            int step = 0;
            int count = 0;

            for(int i=0; i<=C5Model.numOfMol; i++){
              if(bestQ < Mol[i].q) bestQ=Mol[i].q;
            }
            step = Math.abs((C5Model.qualityMax-C5Model.qualityCheck))/ C5Model.numOfSubMKT;
            for(int i=0; i<C5Model.numOfSubMKT; i++) {
                sMKT[i].qMinReq = count*step + C5Model.qualityCheck;
                count= count + 1;
            }
        }
}

//products
class Product{
    //it is the quality of the product
    double qp, 
    //it is teh amount of marketing investment        
            m, 
    //Shares of the product within the TC
            share, 
            shareP, 
    //Product utility            
            pos,  
    //Product markup           
            mup, 
   //number of patients reached by the product            
            numPatients ;
    //TC and molecule IDs
    int TC, mol, 
    //Period when the product enters the market
            BProd, 
    //Difference between the the period when the product enters the market and the time when the patent is granted         
            EDP, 
    //submarkets of the TC where the product is sold        
            subMKT;
    boolean 
            //imitative of innovative product
            imitative, 
            //true, when the product exit the market
            out=false;   
    //simualtion paremeter for marketing investment erosion
    double erosionMarketing = C5Model.erosion; 
    //time requested for the full development of the product
    int devPeriod = 0; 
    //vectors that record the history of the product
    double[] historyEarnings = new double[C5Model.endTime+1];
    double[] historyPatients = new double[C5Model.endTime+1];
    double[] subMKTvalue = new double[C5Model.numOfSubMKT];

    Product(int QP, double M, double MUP, int TA, int MOL, boolean IMI, int birthdayProd) {         
	qp	    = QP; 
	m	    = M;
	mup	    = MUP;
	TC	    = TA;
	mol	    = MOL;
	imitative   = IMI;
	BProd	    = birthdayProd;        
     }

//definition of the utility function
    public void probOfSell(int t, int firm) {   
        pos = 0;      
            //see equation 8 in chapter 5
            m = 1 + m * (1 - erosionMarketing);
            //see equation 5 for the price calculation
            //see equation 9 in chapter 5
            pos = Math.pow(qp, C5Model.TC[TC].a) * Math.pow((1 / (C5Model.costProd * (1 + mup))), C5Model.TC[TC].b) * Math.pow(m, C5Model.TC[TC].c);             
    }

}

class Firm {
    double budget,
            //innate propensity to be an innovator or an imitator
            imin,
            //interests amount
            interests,
            //as defined by the simulation parameters, equal for all firms
            costOfInno,
            costOfImi,
            //patients reached by the firm with all its drugs
            totalReachedPatients,              
            //Purcentage of R&D budget devoted to search activity
            alfa,
            //total cost of development activities in current period
            totcostt,       
            //accoutning variables
            mkting,                       
            search_research,            
            budgetM,            
            budgetRes,            
            totProfit,                                    
            searchExpenditure,
            researchExpenditure,
            VtotTAMkting=0,            
            totTC;
    
            
            int 
            numOfProducts,
            onMol,
            ntcF, 
            mktingInv = 0, 
            //number of products / patients
            numInno=0, 
            numImi=0, 
            totProd=0, 
            pInno=0, 
            pImi=0;
           
            boolean
            alive,
            innovator,
            innovatort,
            nowInno,
            onMkt;
    
    Product[] Prod = new Product[100000];
    
    double[] totShare = new double[C5Model.endTime+2];

    double[] totShareQuantity = new double[C5Model.endTime+2];
    
    int[] counterTa;

    double[] shTC = new double[C5Model.numOfTC];
    double[] shTA1 = new double[C5Model.numOfTC];
    searchAction SearchAction = new searchAction();
    Memory onProInno = new Memory(); 
    Memory onProImi = new Memory();
    Memory mktingVet = new Memory();
    multiprojectselection mProj = new multiprojectselection();

    Firm(double BUD, double MKT, double SEARCH_RESEARCH, double ALFA, int NTC, boolean INNOVATORFIRM,double IMIN){         
	budget		    	= BUD;
	alfa		    	= ALFA;
        mkting		    	= MKT;
	search_research	    	= SEARCH_RESEARCH;
	numOfProducts	    	= 0;
	alive		    	= false;
	ntcF		    	= NTC;
	innovator		= INNOVATORFIRM;
	counterTa	    	= new int[ntcF+1];
        onMkt                   = false;
        imin                    = IMIN;

	for(int i=0;i<=ntcF; i++) counterTa[i]=0;
    }

   //choose imitation or innovation routines
    public boolean chooseImIn(){
        boolean c;
           if(this.imin<=C5Model.r.nextDouble()) c=true;
            else c=false;        
           return c;
    }

    /*Claulate the number of innovative and imitative products*/
    public void clacImiInno(int t){
        this.numInno=0;
        this.numImi=0;
        this.pInno=0;
        this.pImi=0;
        for(int i=1; i<=this.numOfProducts; i++){
            if(this.Prod[i].imitative==false && this.Prod[i].out==false){
                this.numInno++;
                this.pInno+=this.Prod[i].historyEarnings[t-1];
            }
            if(this.Prod[i].imitative==true && this.Prod[i].out==false){
                this.numImi++;
                this.pImi+=this.Prod[i].historyEarnings[t-1];
            }
        }
        this.totProd=this.numImi+this.numInno;
    }

    //the firm decides how many research projects it wants to run simultaneously
    public int numprojects(boolean In,double timedev){
        double b = this.budgetRes;
        int nproj=0;
        if(alive==true){ 
            
     for(int i=0; i<this.onProInno.MemOfTC.length; i++){
         if(this.onProInno.done[i]==false){
             b=b-(this.costOfInno * this.onProInno.on[i] * (timedev-this.onProInno.state[i]));
         }
        }

     for(int i=0; i<this.onProImi.MemOfTC.length; i++){
         if(this.onProImi.done[i]==false){
             b=b-(this.costOfImi * this.onProImi.on[i] * (timedev-this.onProImi.state[i]));
         }
     }

     if(In==true)
            //see equation 3 in chapter 5
            nproj = (int) (b/(timedev*this.costOfInno));
     else
            nproj = (int) (b/(timedev*this.costOfImi));
        }
        if(nproj<0)
            nproj=0;

     return nproj;
    }

    public void search(int Time, String st, double drawC){
                this.SearchAction.numberDraw=0;
                this.searchExpenditure=0;
        if(st.equals("inno")){
            //only the first period 90% of the budget is assigned to research
                  if(Time==1){
                       budgetRes	        = budget*0.9;
                       budgetM                  = budget*0.1;
                  }
    
           this.costOfInno=C5Model.costOfResearchInn;
           this.costOfImi=C5Model.costOfResearchImi;
           double b = this.budgetRes;
    
    // calculate (and set aside) the budget that has to be used for the current development activities and subtract the total from the budget available
     for(int i=0; i<this.onProInno.MemOfTC.length; i++){
         if(this.onProInno.done[i]==false){
             b=b-(this.costOfInno * this.onProInno.on[i] * (C5Model.timeDevelop-this.onProInno.state[i]));
         }
        }
     for(int i=0; i<this.onProImi.MemOfTC.length; i++){
         if(this.onProImi.done[i]==false){
             b=b-(this.costOfImi * this.onProImi.on[i] * (C5Model.timeDevelop-this.onProImi.state[i]));
         }
     }
    //the budget left is multiplied by the proportion that is devoted to seacrh activities
                  searchExpenditure   = b * alfa;
                  //updates the R&D budget
                  budgetRes -= (searchExpenditure+C5Model.costOfSearch);
                  //updates the budget
                  budget=budgetM+budgetRes;
        }
        if(st.equals("imi")){
                   budget=budgetM+budgetRes;
        }
    }

    //the firm exits the market
    public void failure(){
	alive = false;

	for(int i=0;i<=ntcF; i++) counterTa[i]=0;
	numOfProducts	= 0;
	totProfit	= 0;
	budget		= 0;
	budgetRes	= 0;
	budgetM		= 0;
	ntcF		= 0;
    }

    //the firm calculates its interests according to the simulation interest rate
    public void interest(double rate){ 
        interests=0;
        interests+=this.budgetRes*rate;
        interests+=this.budgetM*rate;
           if(this.mktingInv==0){
                budgetRes += interests;
                }
                else {
                budgetM += mkting * interests;
                budgetRes += search_research * interests;
             }
    }

    public int selectMol(int[] ta, int po, Memory onI){
        int bestPo=0;
        double sum=0;
        double[] MolProb= new double [onI.MemOfTC.length];

        if(ta[onI.MemOfTC[po]]>1){
              for(int t=0; t<onI.MemOfTC.length; t++){
                  if(onI.MemOfTC[po]==onI.MemOfTC[t]
                          && onI.on[t]==0){
                      MolProb[t]=C5Model.TC[onI.MemOfTC[t]].Mol[onI.MemOfMol[t]].q;
                  }
              }

              for(int tot=0; tot<MolProb.length; tot++){
                  sum+=MolProb[tot];
              }

              for(int tot=0; tot<MolProb.length; tot++){
                  MolProb[tot]=(MolProb[tot]/sum);
              }

              double casual=C5Model.r.nextDouble();
              double ti=0;
              boolean exit=false;

              for(int bp=0; bp<MolProb.length; bp++){
                  if(exit==false){
                      ti+=MolProb[bp];
                      if(exit==false && ti>casual){
                          exit=true;
                          bestPo=bp;
                      }
                  }
              }
            }

        else bestPo=po;
            return bestPo;
    }

    //the products below a certaing market share "outLev" exit the market
    public void productsOut(double outLev){
        for(int i=1; i<=this.numOfProducts; i++){
         if(this.Prod[i].share<outLev && this.Prod[i].out==false)
             this.Prod[i].out=true;
        }
    }

    public void research(int t){
        double totcost=0;
            for(int i=0; i<this.onProInno.MemOfTC.length; i++){
                if(this.onProInno.done[i]==false){
                totcost+=(this.onProInno.on[i]*this.onProInno.weight[i]*this.costOfInno);
                if(this.onProInno.on[i]==1 && this.onProInno.state[i]==0) this.onProInno.timeSv[i]=t;               
                this.onProInno.state[i]+=(this.onProInno.on[i]*this.onProInno.weight[i]);
                }
            }

             for(int i=0; i<this.onProImi.MemOfTC.length; i++){
                if(this.onProImi.done[i]==false){
                totcost+=(this.onProImi.on[i]*this.onProImi.weight[i]*this.costOfImi);           
                if(this.onProImi.on[i]==1 && this.onProImi.state[i]==0) this.onProImi.timeSv[i]=t;
                this.onProImi.state[i]+=(this.onProImi.on[i]*this.onProImi.weight[i]);
                }
             }

             budgetRes = budgetRes - totcost;
             totcostt=totcost;

             if(((this.alive==true) && (this.numOfProducts==0)
             && totcost==0 && budgetRes<(C5Model.timeDevelop*C5Model.costOfResearchImi)           
             )){
                failure();
            }

        budget=budgetRes+budgetM;
       }

    //assignes marketing budget to each product according to the state of development
    public void ProjMkting(){
        this.VtotTAMkting=0;
        this.mktingInv=0;

            for(int i=0; i<this.onProInno.MemOfTC.length; i++){
                if(this.onProInno.done[i]==false){
                    if(((this.onProInno.state[i]*C5Model.TC[this.onProInno.MemOfTC[i]].Mol[this.onProInno.MemOfMol[i]].q)/C5Model.timeDevelop)>C5Model.accMkting){
                       this.mktingInv++;
                       this.VtotTAMkting+=this.onProInno.value[i];
                     }
                    }
                  }

            for(int i=0; i<this.onProImi.MemOfTC.length; i++){
                if(this.onProImi.done[i]==false){
                    if(((this.onProImi.state[i]*C5Model.TC[this.onProImi.MemOfTC[i]].Mol[this.onProImi.MemOfMol[i]].q)/C5Model.timeDevelop)>C5Model.accMkting){
                       this.mktingInv++;
                       this.VtotTAMkting+=this.onProImi.value[i];
                    }
                    }
                  }
    }

//Updates marketing budget
public void mkting(){
        double bM = this.budgetM;
                    for(int i=0; i<this.onProInno.MemOfTC.length; i++){
                    if(this.onProInno.done[i]==false){
                    if(((this.onProInno.state[i]*C5Model.TC[this.onProInno.MemOfTC[i]].Mol[this.onProInno.MemOfMol[i]].q)/C5Model.timeDevelop)>C5Model.accMkting){
                             bM-=this.onProInno.mktingVet[i];
                          }
                       }
                    }
                for(int i=0; i<this.onProImi.MemOfTC.length; i++){
                if(this.onProImi.done[i]==false){
                    if(((this.onProImi.state[i]*C5Model.TC[this.onProImi.MemOfTC[i]].Mol[this.onProImi.MemOfMol[i]].q)/C5Model.timeDevelop)>C5Model.accMkting){
                          bM-=this.onProImi.mktingVet[i];
                         }
                      }
                  }

            for(int i=0; i<this.onProInno.MemOfTC.length; i++){
                if(this.onProInno.done[i]==false){
                    if(((this.onProInno.state[i]*C5Model.TC[this.onProInno.MemOfTC[i]].Mol[this.onProInno.MemOfMol[i]].q)/C5Model.timeDevelop)>C5Model.accMkting){
                                 this.onProInno.mktingVet[i]+=(bM*(this.onProInno.value[i]/this.VtotTAMkting));
                     }
                    }
                  }       
            for(int i=0; i<this.onProImi.MemOfTC.length; i++){
                if(this.onProImi.done[i]==false){
                    if(((this.onProImi.state[i]*C5Model.TC[this.onProImi.MemOfTC[i]].Mol[this.onProImi.MemOfMol[i]].q)/C5Model.timeDevelop)>C5Model.accMkting){
                             this.onProImi.mktingVet[i]+=(bM*(this.onProImi.value[i]/this.VtotTAMkting));
                     }
                    }
                  }
        budget=budgetM+budgetRes;
}

    public void newProduct(int QP, double M, double MUP, int TA, int MOL, boolean IMIT, int FOCAL, int TPRODBORN, int timeDev){ 

        boolean temp;      
	numOfProducts++; 
	Prod[numOfProducts] = new Product(QP, M, MUP, TA, MOL, IMIT, TPRODBORN);

        if(C5Model.TC[TA].Mol[MOL].productsOn==0) temp=false;
        else temp=true;
        C5Model.TC[TA].prodInTC++;
        C5Model.TC[TA].Mol[MOL].productsOn += 1;
        Prod[numOfProducts].imitative =  temp;   
        if(Prod[numOfProducts].imitative==false) Prod[numOfProducts].EDP=Prod[numOfProducts].BProd-C5Model.TC[Prod[numOfProducts].TC].Mol[Prod[numOfProducts].mol].patentTime;
        this.Prod[numOfProducts].devPeriod=timeDev;
        budgetM=budgetM-M; 
        budget=budgetRes+budgetM;
    }

     public void numOfTa(){ 
	totTC =0;
	for(int i=0;i<=ntcF; i++) counterTa[i]=0;
	for(int i=1; i<= numOfProducts; i++){
	   if(this.Prod[i].out==false) counterTa[Prod[i].TC]=1;
	}
	for (int i = 0; i<= ntcF; i++)
	    totTC += counterTa[i];
    }

    public void accounting(){          
            budget += totProfit;

            if(this.mktingInv==0){
                budgetRes += totProfit;
                }

            else {
                budgetM += mkting * totProfit;
                budgetRes += search_research * totProfit;
             }
	    }

    public class searchAction { 
    int badperf;
    int[] portfolioTC;
    int[] portfolioMol;
    int numberDraw;
   
    searchAction() {

    }
//the firm draws new molecules
    public void createPortfolioMolTa(int t, int prod, double alfa_cum) {
   //this is the standard method of drawing new molecules (no cumulativeness in the search process)
   if(C5Model.draw1==false){
        if((alive == true)){	           
                    if (searchExpenditure > C5Model.drawCost){
                        badperf=0;
                        numberDraw = (int) Math.round((searchExpenditure/C5Model.drawCost));
                    }
                    else {
                        numberDraw = 0;
                        badperf++;
                    }
                    
                    // if the firm does not find a promising molecule after "C5Model.searchFailure" number of draws, it fails
                    if(badperf>C5Model.searchFailure) {
                        failure();
                    }
                    
                    // for each draw we add a cell to the array of promosing molecules drawn (portfolioTC/portfolioMol)
                    //a new portfolio of molecules is created for each single search activity
                        portfolioTC = new int[numberDraw+1];
                        for(int y = 0; y < numberDraw; y++) portfolioTC[y] = -2;                     
                        for(int n = 0; n < numberDraw; n++) portfolioTC[n] = (int) Math.round(C5Model.r.nextDouble()*(C5Model.numOfTC-1));
         
                        portfolioMol = new int[numberDraw+1];
                        for(int y = 0; y < numberDraw; y++) portfolioMol[y] = -3;         
                        for(int n = 0; n < numberDraw; n++) portfolioMol[n] = (int) Math.round(C5Model.r.nextDouble()*(C5Model.numOfMol));

        }
      }
   
      //this is the alternative method of drawing new molecules. We include cumulativeness in the search process
      if(C5Model.draw1==true){
           if((alive == true)){	           
                    if (searchExpenditure > C5Model.drawCost){
                        badperf=0;
                        //see equation 13 in chapter 5
                        numberDraw = (int) (Math.round((searchExpenditure/C5Model.drawCost))+(alfa_cum*prod));
                    }
                    else {
                        numberDraw = 0;
                        badperf++;
                    }

                    if(badperf>C5Model.searchFailure) { 
                        failure();
                    }            
                        portfolioTC = new int[numberDraw+1];
                        for(int y = 0; y < numberDraw; y++) portfolioTC[y]=-2;                        
                        for(int n = 0; n < numberDraw; n++) portfolioTC[n] = (int) Math.round(C5Model.r.nextDouble()*(C5Model.numOfTC-1));           

                        portfolioMol = new int[numberDraw+1];
                        for(int y = 0; y < numberDraw; y++) portfolioMol[y]=-3;                        
                        for(int n = 0; n < numberDraw; n++) portfolioMol[n] = (int) Math.round(C5Model.r.nextDouble()*(C5Model.numOfMol));
        }
      }      
 }
    //the firm select an innovative behaviour and searches for new molecules to patent and develop
    public void doSearch(int t, int prod) {     
       numberDraw        =   0;
       //it creates a portfolio of drawn molecules 
       createPortfolioMolTa(t, prod, C5Model.alfa_cumulativeness);
       //it records the portfolio of drawn molecules in the array where the firm stores all 
       //the molecules that are potentially attractive for the innovative activity "onProInno" 
       onProInno.recordMemory(portfolioMol, portfolioTC, numberDraw);
    }
    
    }

    //this class represents the objects "Memory" that are used to record the molecules drawn during the search activity and the development of imitative or innovative products
    public class Memory {
        int[] MemOfMol = new int[0];
        int[] MemOfTC = new int[0];
        int[] mktingVet = new int[0];
        int[] state = new int[0];
        int[] on = new int[0];
        int[] weight = new int[0];
        int[] value = new int[0];
        int[] timeSv = new int[0];
        boolean[] done = new boolean[0];

        int[] swapResMemOfMol = new int[0];
        int[] swapResMemOfTa = new int[0];
        int[] swapMktingVet = new int[0];
        int[] swapState = new int[0];
        int[] swapOn = new int[0];
        int[] swapPeso = new int[0];
        int[] swapValore = new int[0];
        int[] swapTimeSv = new int[0];
        boolean[] swapDone = new boolean[0];

        public void addElement(int ta, int mol) { 
            boolean in = false;
            int length = MemOfMol.length;
            for(int i=0; i<length; i++) {
                 if(MemOfMol[i] == mol && MemOfTC[i] == ta) {
                     in = true;
                 }
            }

            if(in == false) {
            swapResMemOfTa = new int[length];
            swapResMemOfMol = new int[length];
            swapMktingVet = new int[length];
            swapState = new int[length];
            swapOn = new int[length];
            swapPeso = new int[length];
            swapValore = new int[length];
            swapTimeSv = new int[length];
            swapDone = new boolean[length];

            for(int i=0; i<length; i++) {
                swapResMemOfTa[i] = MemOfTC[i];
                swapResMemOfMol[i] = MemOfMol[i];
                swapMktingVet[i] = mktingVet[i];
                swapState[i] = state[i];
                swapOn[i] = on[i];
                swapPeso[i] = weight[i];
                swapValore[i] = value[i];
                swapTimeSv[i] = timeSv[i];
                swapDone[i] = done[i];
            }

            MemOfMol = new int[length+1];
            MemOfTC  = new int[length+1];
            mktingVet = new int[length+1];
            state = new int[length+1];
            on = new int[length+1];
            weight = new int[length+1];
            value = new int[length+1];
            timeSv = new int[length+1];
            done = new boolean[length+1];

            for(int i=0; i<length; i++) {
                MemOfMol[i] = swapResMemOfMol[i];
                MemOfTC[i] = swapResMemOfTa[i];
                mktingVet[i] = swapMktingVet[i];
                state[i] = swapState[i];
                on[i] = swapOn[i];
                weight[i] = swapPeso[i];
                value[i] = swapValore[i];
                timeSv[i] = swapTimeSv[i];
                done[i] = swapDone[i];
            }

            MemOfMol[length] = mol;
            MemOfTC[length] = ta;
            mktingVet[length] = 0;
            state[length] = 0;
            on[length] = 0;
            weight[length] = 0;
            value[length] = 0;
            timeSv[length] = 0;
            done[length] = false;
            }
        }

        public boolean controlMol(int mol, int ta) { 
            if(                   (C5Model.TC[ta].Mol[mol].q >=1)
                               && (C5Model.TC[ta].Mol[mol].nowFree == false)
                               && (C5Model.TC[ta].Mol[mol].patent == false)) return true;
            else return false;
        }

        public void recordMemory(int[] portfolioMol ,int[] portfolioTa, int numberDraw) { 
            for(int i=0; i<numberDraw; i++){
                if(controlMol(portfolioMol[i],portfolioTa[i])==true) onProInno.addElement(portfolioTa[i], portfolioMol[i]);
                }

        }

        public void recordMemoryImi() { 
            for(int i=0; i<C5Model.numOfTC; i++){
                   for(int ii=0; ii<=C5Model.numOfMol; ii++){
                        if(C5Model.TC[i].Mol[ii].patent==false
                                && C5Model.TC[i].Mol[ii].nowFree==true
                                && C5Model.TC[i].Mol[ii].productsOn>0                            
                                ) onProImi.addElement(i,ii);
                }

        }


    }

} 

} 

//this class contains methods to select the most promising projects
final class multiprojectselection{
  public static boolean inVet(int[] vetTA,int[] vetMol, int ta, int mol){
      boolean in=false;
      for(int v=0; v<vetTA.length; v++){
          if(
                  vetMol[v]==mol &&
                  vetTA[v]==ta){
              in=true;
          }
      }
      return in;
  }
  public static void orderValue(int[] val, int cap, int f, int t){
                  for(int count=0; count<cap; count++){
                      
                      int posBest=-1;
                      int c=0;
                      int[] Ta = new int[C5Model.numOfTC];

                      if(C5Model.F[f].nowInno==true){
                      double vtot=0;

                      for(int i=0; i<C5Model.F[f].onProInno.MemOfTC.length; i++){
                          if(C5Model.F[f].onProInno.on[i]==0){
                              double multiplier=((C5Model.patentDuration-(t-C5Model.TC[C5Model.F[f].onProInno.MemOfTC[i]].Mol[C5Model.F[f].onProInno.MemOfMol[i]].patentTime))/(C5Model.patentDuration)); 
                              if(C5Model.TC[C5Model.F[f].onProInno.MemOfTC[i]].Mol[C5Model.F[f].onProInno.MemOfMol[i]].patentBy==f
                                   && multiplier>0) multiplier=multiplier;
                              else multiplier=0;
                              //see equation 4 in chapter 5
                              vtot+=C5Model.F[f].onProInno.value[i]*multiplier;
                              c++;
                              Ta[C5Model.F[f].onProInno.MemOfTC[i]]++;
                          }
                      }

                      if(c>0){
                          double casual=C5Model.r.nextDouble();
                          double ti=0;
                          boolean exit=false;
                          for(int i=0; i<C5Model.F[f].onProInno.MemOfTC.length; i++){
                                if(C5Model.F[f].onProInno.on[i]==0
                                        && exit==false){
                              double multiplier=((C5Model.patentDuration-(t-C5Model.TC[C5Model.F[f].onProInno.MemOfTC[i]].Mol[C5Model.F[f].onProInno.MemOfMol[i]].patentTime))/(C5Model.patentDuration));
                              if(C5Model.TC[C5Model.F[f].onProInno.MemOfTC[i]].Mol[C5Model.F[f].onProInno.MemOfMol[i]].patentBy==f
                                   && multiplier>0) multiplier=multiplier;
                              else multiplier=0;
                                  ti+=(C5Model.F[f].onProInno.value[i]*multiplier/vtot);
                                  if(exit==false && ti>casual){
                                      exit=true;
                                      posBest=C5Model.F[f].selectMol(Ta, i, C5Model.F[f].onProInno);
                                  }
                                }
                          }
                      }


                     if(posBest!=-1){
                          C5Model.F[f].onProInno.on[posBest]=1;
                          C5Model.TC[C5Model.F[f].onProInno.MemOfTC[posBest]].Mol[C5Model.F[f].onProInno.MemOfMol[posBest]].onMolRes++;
                          C5Model.TC[C5Model.F[f].onProInno.MemOfTC[posBest]].onTaRes++;
                        }
                      }

                      if(C5Model.F[f].nowInno==false){
                      double vtot=0;

                      for(int i=0; i<C5Model.F[f].onProImi.MemOfTC.length; i++){
                          if(C5Model.F[f].onProImi.on[i]==0 &&
                               (inVet(C5Model.F[f].onProInno.MemOfTC,
                                    C5Model.F[f].onProInno.MemOfMol,
                                    C5Model.F[f].onProImi.MemOfTC[i],
                                    C5Model.F[f].onProImi.MemOfMol[i]))==false){
                              vtot+=C5Model.F[f].onProImi.value[i];
                              c++;
                              Ta[C5Model.F[f].onProImi.MemOfTC[i]]++;
                          }
                      }



           if(c>0){
                          double casual=C5Model.r.nextDouble();
                          double ti=0;
                          boolean exit=false;
                          for(int i=0; i<C5Model.F[f].onProImi.MemOfTC.length; i++){
                                if(C5Model.F[f].onProImi.on[i]==0
                                        && exit==false &&
                               (inVet(C5Model.F[f].onProInno.MemOfTC,
                                    C5Model.F[f].onProInno.MemOfMol,
                                    C5Model.F[f].onProImi.MemOfTC[i],
                                    C5Model.F[f].onProImi.MemOfMol[i]))==false){
                                  ti+=(C5Model.F[f].onProImi.value[i]/vtot);
                                  if(exit==false && ti>casual){
                                      exit=true;
                                      posBest=C5Model.F[f].selectMol(Ta, i, C5Model.F[f].onProImi);
                                  }
                                }
                          }
                      }

                      if(posBest!=-1){
                          C5Model.F[f].onProImi.on[posBest]=1;
                          C5Model.TC[C5Model.F[f].onProImi.MemOfTC[posBest]].Mol[C5Model.F[f].onProImi.MemOfMol[posBest]].onMolRes++;
                          C5Model.TC[C5Model.F[f].onProImi.MemOfTC[posBest]].onTaRes++;
                      }
                      }

              }
 }
  public static void in( int[] pesi, int[] valore, int capacita, int f,int t) {

    int [] weight = pesi;
    int [] value =  valore;
    int capacity = capacita;

    orderValue(value, capacity, f, t);
  }
}



final class statistic {

    static double[][] zeros             ; 
    static double[][][] tat             ; 
    static double[][][] taDimSingle     ; 
    static double[][][] firmt            ; 
    static double[][][] firmFeat            ; 
    static double[][] totProdinmkt	    	;
    static double[][] totfbudget	    	;
    static double[] meanFTA ;
    static double[] meanFTAinno ;
    static double[] meanFTAimi ;
    static double[] prodMeanFirm         ;
    static double[] totH	        ;
    static double[] totHQuantity        ;
    static double[] meanH	    	;
    static double[] meanH1	    	;
    static double[] meanTaDim           ;
    static double[] profitTot           ;
    static double[] meanTaPat           ;
    static double[] TaViewed	    	;
    static double[] totFinTa	    	;
    static double[] totFinTainno	    	;
    static double[] totFinTaimi	    	;
    static double[] imiProd	    	;
    static double[] innoProd	    	;
    static double[] qInno	    	;
    static double[] size		;
    static double[] sizeInc		;
    static double[] firmLeader            ;
    static double[] leaderStability            ;
    static double[] redsales            ;
    static double[] redsales1            ;
    static double[] innoSize            ;
    static double[] imiSize             ;
    static double[] innoSh           ;
    static double[] imiSh             ;
    static double[] sizeNBF		;
    static double[] outProd		;
    static double[] imiNumber	    	;
    static double[] innoNumber	    	;
    static double[] imiNature	    	;
    static double[] innoNature	    	;
    static double[] aliveF              ;
    static double[] aliveFwithProd      ;
    static double[] priceMean           ;
    static double[] priceMeanInno       ;
    static double[] priceMeanImi        ;
    static double[] g                   ;
    static double[] gInno	    	;
    static double[] gImi	    	;
    static double[] countSVIL           ;
    static double[] countSvilInno	;
    static double[] countSvilImi        ;
    static double[] aliveIncumbentFirm	;
    static double[] aliveNBF	    	;
    static double[] NumInnoFirm         ;
    static double[] NumImiFirm         ;

    // array used in multi time simulation
    static double[] multiTotH		;
    static double[] multiTotHQuantity   ;
    static double[] multiMeanH		;
    static double[] multiMeanH1		;
    static double[] multiImiProd	;
    static double[] multiInnoProd	;
    static double[] multiQInno	;
    static double[] multiImiNumber	;
    static double[] multiInnoNumber	;
    static double[] multiImiNature	;
    static double[] multiInnoNature	;
    static double[] multiPrice          ;
    static double[] multiPriceInno      ;
    static double[] multiPriceImi       ;
    static double[] multiG              ;
    static double[] multiGInno          ;
    static double[] multiGImi           ;
    static double[] multiCount          ;
    static double[] multiCountInno      ;
    static double[] multiCountImi       ;
    static double[] multiAliveF		;
    static double[] multiAliveFwithProd ;
    static double[] multiTaViewed	;
    static double[] multiSizeInc	;
    static double[] multiSizeNBF	;
    static double[] multiSize		;
     static double[] multiLeaderStability       ;
     static double[] multiredsales       ;
     static double[] multiredsales1       ;
    static double[] multiInnoSize       ;
    static double[] multiImiSize        ;
    static double[] multiAliveIncumbentFirm	;  
    static double[] multiAliveNBF	;
    static double[] multiAgree          ;
    static double[] multiNumInnoFirm	;  
    static double[] multiTaDim          ;
    static double[] multiTaPat          ;
    static double[] multiPrTot          ;
    static double[] multiOutProd        ;

     public statistic() {

    }

     public static void initValue(int end, int numOfTain,int numOfFirmin){
         C5Model.stab=0;

         for(int p=0; p<12; p++)
         for (int i=0; i<end; i++){
            zeros[i][p]=0;
        }


	for (int i=0 ; i<=end+1; i++){
        for (int ii=0; ii<(numOfTain); ii++){
                tat[i][ii][0]  =0; //FIRMS
                tat[i][ii][1]  =0; //PRODUCTS
                tat[i][ii][2]  =0; //INNO FIRMS
                tat[i][ii][3]  =0; //IMI FIRMS
            }
        for (int ii=0; ii<(numOfTain); ii++){
                taDimSingle[i][ii][0]  =0; 
                taDimSingle[i][ii][1]  =0;
            }
        for (int ii=0; ii<(numOfFirmin); ii++){
                firmt[i][ii][0] =0; //inno
                firmt[i][ii][1] =0; //imi
                totProdinmkt [i][ii] =0  	;
            }
        for (int ii=0; ii<(numOfFirmin); ii++){
            for (int m=0; m<7; m++){
                firmFeat[i][ii][m] =0; //inno                          
                           }
            }

        for (int ii=0; ii<(numOfFirmin); ii++){
                firmt[i][ii][0] =0; //inno
                firmt[i][ii][1] =0; //imi
                totfbudget [i][ii] =0  	;
            }


	    totH[i]			= 0;
            prodMeanFirm[i]           =0;
            totHQuantity[i]             = 0;
            meanTaDim[i] =0;
            profitTot[i] =0;
            meanTaPat[i]=0;
            meanFTA[i] =0;
            meanFTAinno[i] =0;
            meanFTAimi[i] =0;
	    meanH[i]			= 0;
            meanH1[i]			= 0;
	    TaViewed[i]			= 0;
            totFinTa[i]			= 0;
            totFinTainno[i]			= 0;
            totFinTaimi[i]			= 0;
	    imiProd[i]			= 0;
	    innoProd[i]			= 0;
            qInno[i]			= 0;
            imiNumber[i]			= 0;
	    innoNumber[i]			= 0;
            imiNature[i]			= 0;
	    innoNature[i]			= 0;
	    size[i]			= 0;
            firmLeader[i]                 = 0;
            leaderStability[i]                 = 0;
            redsales[i]                 = 0;
            redsales1[i]                 = 0;
            innoSize[i]                 = 0;
            imiSize[i]                  = 0;
            innoSh[i]                 = 0;
            imiSh[i]                  = 0;
	    sizeInc[i]			= 0;
	    sizeNBF[i]			= 0;
            outProd[i]                  = 0;
            aliveF[i]                   = 0;
            aliveFwithProd[i]           = 0;
            priceMean[i]                = 0;
            priceMeanInno[i]            = 0;
            priceMeanImi[i]             = 0;
            g[i]                        = 0;
            gInno[i]	    	        = 0;
            gImi[i]	    	        = 0;
            countSVIL[i]                = 0;
            countSvilInno[i]	        = 0;
            countSvilImi[i]             = 0;
            aliveIncumbentFirm[i]	= 0;
            aliveNBF[i]	    	        = 0;
            NumInnoFirm[i]              = 0;
            NumImiFirm[i]              = 0;
	}
    }

     public static void createArray(int end, int ta, int firm) { 
     zeros                      = new double[end+2][12];
     tat                        = new double[end+2][ta+1][4];
     taDimSingle                = new double[end+2][ta+1][2];
     firmt                      = new double[end+2][firm][2];
     firmFeat                      = new double[end+2][firm][7];
     totProdinmkt               = new double[end+2][firm];
     totfbudget               = new double[end+2][firm];
    // array used in single time simulation
     totH			= new double[end+2];
     meanFTA                    = new double[end+2];
     meanFTAinno                    = new double[end+2];
     meanFTAimi                    = new double[end+2];
     prodMeanFirm		= new double[end+2];
     totHQuantity               = new double[end+2];
     meanTaDim                  = new double[end+2];
     profitTot                  = new double[end+2];
     meanTaPat                  = new double[end+2];
     meanH	    		= new double[end+2];
     meanH1	    		= new double[end+2];
     TaViewed	    		= new double[end+2];
     totFinTa	    		= new double[end+2];
        totFinTainno	    		= new double[end+2];
           totFinTaimi	    		= new double[end+2];
     imiProd	    		= new double[end+2];
     innoProd	    		= new double[end+2];
        qInno	    		= new double[end+2];
      imiNumber	    		= new double[end+2];
     innoNumber	    		= new double[end+2];
      imiNature	    		= new double[end+2];
     innoNature	    		= new double[end+2];
     size			= new double[end+2];
     firmLeader			= new double[end+2];
     leaderStability		= new double[end+2];
     redsales		= new double[end+2];
     redsales1		= new double[end+2];
     innoSize                   = new double[end+2];
     imiSize                    = new double[end+2];
     innoSh                     = new double[end+2];
     imiSh                      = new double[end+2];
     sizeInc			= new double[end+2];
     sizeNBF			= new double[end+2];
     outProd                    = new double[end+2];

     aliveF                     = new double[end+2];
     aliveFwithProd             = new double[end+2];
     priceMean                  = new double[end+2];
     priceMeanInno              = new double[end+2];
     priceMeanImi               = new double[end+2];
     g                          = new double[end+2];
     gInno	                = new double[end+2];
     gImi	                = new double[end+2];
     countSVIL                  = new double[end+2];
     countSvilInno	        = new double[end+2];
     countSvilImi               = new double[end+2];
     aliveIncumbentFirm	        = new double[end+2];
     aliveNBF	    	        = new double[end+2];
     NumInnoFirm                = new double[end+2];
     NumImiFirm                = new double[end+2];

    // array used in multi time simulation
     multiTotH			= new double[end+2];
     multiTotHQuantity		= new double[end+2];
     multiTaDim                 = new double[end+2];
     multiTaPat                 = new double[end+2];
     multiPrTot                 = new double[end+2];
     multiMeanH			= new double[end+2];
     multiMeanH1		= new double[end+2];
     multiImiProd		= new double[end+2];
     multiImiNumber		= new double[end+2];
     multiImiNature		= new double[end+2];
     multiPrice                 = new double[end+2];
     multiInnoProd              = new double[end+2];
     multiQInno              = new double[end+2];
     multiInnoNumber            = new double[end+2];
     multiInnoNature            = new double[end+2];
     multiPriceInno             = new double[end+2];
     multiPriceImi              = new double[end+2];
     multiG                     = new double[end+2];
     multiGInno                 = new double[end+2];
     multiGImi                  = new double[end+2];
     multiCount                 = new double[end+2];
     multiCountInno             = new double[end+2];
     multiCountImi              = new double[end+2];
     multiAliveF		= new double[end+2];
     multiAliveFwithProd 	= new double[end+2];
     multiTaViewed		= new double[end+2];
     multiSizeInc		= new double[end+2];
     multiSizeNBF		= new double[end+2];
     multiLeaderStability              = new double[end+2];
     multiredsales              = new double[end+2];
     multiredsales1              = new double[end+2];
     multiInnoSize              = new double[end+2];
     multiImiSize               = new double[end+2];
     multiSize			= new double[end+2];
     multiAliveIncumbentFirm	= new double[end+2];
     multiAliveNBF	        = new double[end+2];
     multiAgree          	= new double[end+2];
     multiNumInnoFirm		= new double[end+2];
     multiOutProd		= new double[end+2];
       }

     public static void initMulti(int end, int ta){ 

         for (int i=0 ; i<=end+1; i++){
            multiTotH[i]		= 0;
            multiTotHQuantity[i]        = 0;
            multiTaDim[i]               = 0;
            multiTaPat[i]               = 0;
	    multiMeanH[i]		= 0;
            multiMeanH1[i]		= 0;
	    multiInnoProd[i]		= 0;
            multiQInno[i]		= 0;
	    multiImiProd[i]		= 0;
            multiInnoNumber[i]		= 0;
	    multiImiNumber[i]		= 0;
            multiInnoNature[i]		= 0;
	    multiImiNature[i]		= 0;
            multiPrice[i]               = 0;
            multiPriceInno[i]           = 0;
            multiPriceImi[i]            = 0;
            multiG[i]                   = 0;
            multiGInno[i]               = 0;
            multiGImi[i]                = 0;
            multiCount[i]               = 0;
            multiCountInno[i]           = 0;
            multiCountImi[i]            = 0;
	    multiAliveF[i]		= 0;
	    multiAliveFwithProd[i]	= 0;
	    multiTaViewed[i]		= 0;
	    multiAliveIncumbentFirm[i]	= 0;
	    multiAliveNBF[i]		= 0;
	    multiSize[i]   		= 0;
                   multiLeaderStability[i]            = 0;
                    multiredsales[i]            = 0;
                    multiredsales1[i]            = 0;
            multiInnoSize[i]            = 0;
            multiImiSize[i]             = 0;
	    multiSizeInc[i]		= 0;
	    multiSizeNBF[i]		= 0;
	    multiAgree[i]	        = 0;
	    multiNumInnoFirm[i]		= 0;
            multiOutProd[i]             = 0;
	}
    }

     public static void statistics(int t, double multiTime, int numOfTa, int numOfMol, int numOfFirm){

	double Qtot=0, totValue=0;
        totValue=0;
	for(int i=0; i<numOfTa;i++){
	    if (t<=90) C5Model.TC[i].value = C5Model.TC[i].value ;
	    if (t>90)  C5Model.TC[i].value = C5Model.TC[i].value ;
	    totValue += C5Model.TC[i].value;
            C5Model.TC[i].setSubMKTValue();
        }

        for(int i=0; i<numOfTa; i++) {
            for(int ii=0; ii<=numOfMol; ii++) {
                Qtot += C5Model.TC[i].Mol[ii].q;
            }
        }

 innoProd[t]=0;
 imiProd[t]=0;
 innoSh[t]=0;
 imiSh[t]=0;
 qInno[t]=0;

    for(int ii=0;ii< numOfFirm; ii++) if((C5Model.F[ii].alive == true)&&(C5Model.F[ii].numOfProducts>0)){
	for(int iii=1; iii<=C5Model.F[ii].numOfProducts; iii++) {
            if(C5Model.F[ii].Prod[iii].out==false){
                totProdinmkt[t][ii]++;
		if (C5Model.F[ii].Prod[iii].imitative == false) innoProd[t]++;
		if (C5Model.F[ii].Prod[iii].imitative == true)  imiProd[t] ++;
                if (C5Model.F[ii].Prod[iii].imitative == false) qInno[t]+=C5Model.F[ii].Prod[iii].qp;
                if (C5Model.F[ii].Prod[iii].imitative == false) innoSh[t]+=C5Model.F[ii].Prod[iii].historyEarnings[t];
                if (C5Model.F[ii].Prod[iii].imitative == true)  imiSh[t]+=C5Model.F[ii].Prod[iii].historyEarnings[t];
            }
            else outProd[t]++;
	}
    }

if(innoProd[t]>0)  qInno[t]=qInno[t]/innoProd[t];
else qInno[t]=0;

 double[] count = new double[C5Model.endTime+1];

	for(int a=0; a<numOfFirm;a++) if((C5Model.F[a].alive==true)&&(C5Model.F[a].budget>0)){ 
            totfbudget[t][a]=C5Model.F[a].budgetRes;
            aliveF[t]++;
            if(C5Model.F[a].pInno>=C5Model.F[a].pImi && (C5Model.F[a].numOfProducts>0)) C5Model.F[a].innovator=true;
            else if((C5Model.F[a].numOfProducts>0)) C5Model.F[a].innovator=false; 

            if(C5Model.F[a].numInno>=C5Model.F[a].numImi && (C5Model.F[a].numOfProducts>0)) innoNumber[t]++; 
            else if((C5Model.F[a].numOfProducts>0)) imiNumber[t]++;

            if(C5Model.F[a].imin<0.5 && (C5Model.F[a].numOfProducts>0)) innoNature[t]++;
            else if((C5Model.F[a].numOfProducts>0)) imiNature[t]++;

	    if(C5Model.F[a].innovator==true && (C5Model.F[a].numOfProducts>0)) NumInnoFirm[t]++;
            if(C5Model.F[a].innovator==false && (C5Model.F[a].numOfProducts>0)) NumImiFirm[t]++;
	    if(C5Model.F[a].numOfProducts>0) aliveFwithProd[t]++;

            double cSvil = 0;
            double cSvilInno = 0;
            double cSvilImi = 0;
            double swapInno =0;
            double swapImi =0;
            double gSImi =0;
            double gSInno =0;
            double gS =0;
            double swap = 0;

	    if(C5Model.F[a].numOfProducts>0) {
	             for(int p=1;p<=C5Model.F[a].numOfProducts; p++){
                         if(C5Model.F[a].Prod[p].out==false){
                               cSvil++;
                           if(C5Model.F[a].Prod[p].imitative==true
                                   ) cSvilImi+=C5Model.F[a].Prod[p].devPeriod;
                           if(C5Model.F[a].Prod[p].imitative==false
                                   ) cSvilInno+=C5Model.F[a].Prod[p].devPeriod;
                           if(C5Model.F[a].Prod[p].imitative==true )
                                      gSImi+=C5Model.F[a].Prod[p].historyEarnings[t];
                           if(C5Model.F[a].Prod[p].imitative==false )
                                       gSInno+=C5Model.F[a].Prod[p].historyEarnings[t];
                           if(C5Model.F[a].Prod[p].imitative==true)
                                        swapImi+=C5Model.costProd*(1+C5Model.F[a].Prod[p].mup); 
                           if(C5Model.F[a].Prod[p].imitative==false)
                                        swapInno+=C5Model.costProd*(1+C5Model.F[a].Prod[p].mup);
                           if(C5Model.TC[C5Model.F[a].Prod[p].TC].Mol[C5Model.F[a].Prod[p].mol].patent==true ){
                                       swap+=C5Model.costProd*(1+C5Model.F[a].Prod[p].mup);
                                       gS+=C5Model.F[a].Prod[p].historyEarnings[t];
                                       count[t]++;
                           }
                          }
	             } //close products

         priceMean[t]+=swap;
         g[t]+=gS;
         countSVIL[t]+=cSvil;
         countSvilImi[t]+=cSvilImi;
         countSvilInno[t]+=cSvilInno;
         gImi[t]+=gSImi;
         gInno[t]+=gSInno;
         priceMeanImi[t]+=swapImi;
         priceMeanInno[t]+=swapInno;
	    }	    //close prod
	}           //close firms
       if(count[t]>0) g[t]=g[t]/count[t];
       else zeros[t][0]++;
       if((innoProd[t])>0) gInno[t]=gInno[t]/(innoProd[t]);
       else zeros[t][1]++;
       if((imiProd[t])>0) gImi[t]=gImi[t]/(imiProd[t]);
       else zeros[t][2]++;
       if(aliveFwithProd[t]>0) countSVIL[t]=countSVIL[t];
       else zeros[t][3]++;
       if(innoProd[t]>0) countSvilInno[t]=countSvilInno[t]/innoProd[t];
       else zeros[t][4]++;
       if(imiProd[t]>0) countSvilImi[t]=countSvilImi[t]/imiProd[t];
       else zeros[t][5]++;
       if(innoProd[t]>0) priceMeanInno[t]=priceMeanInno[t]/(innoProd[t]);
       else zeros[t][6]++;
       if((imiProd[t])>0) priceMeanImi[t]=priceMeanImi[t]/(imiProd[t]);
       else zeros[t][7]++;
       if(count[t]>0) priceMean[t]=priceMean[t]/count[t];
       else zeros[t][8]++;

	double sumS=0;
        double numOfTaViewed = 0;

	for(int i=0;i<numOfTa;i++){
	    for(int ii=0; ii<numOfFirm; ii++) if((C5Model.F[ii].alive == true)&&(C5Model.F[ii].numOfProducts>0)){		
                C5Model.F[ii].shTA1[i] = 0;
		for(int iii=1;iii<=C5Model.F[ii].numOfProducts;iii++) if(C5Model.F[ii].Prod[iii].TC == i
                        && (C5Model.F[ii].Prod[iii].out==false)) {		    
                    C5Model.F[ii].shTA1[i] += C5Model.F[ii].Prod[iii].shareP;
		}
	    }

	}
	for(int i=0;i<numOfTa;i++){
	    for(int ii=0;ii< numOfFirm; ii++) if((C5Model.F[ii].alive == true)&&(C5Model.F[ii].numOfProducts>0)){     
		C5Model.TC[i].Herfindahl[t] += Math.pow(C5Model.F[ii].shTC[i],2);
                C5Model.TC[i].Herfindahl1[t] += Math.pow(C5Model.F[ii].shTA1[i],2);
	    }
	}

//number of TC viewed
	for(int i=0; i<numOfTa;i++){
	    if(C5Model.TC[i].Herfindahl[t]>0) numOfTaViewed++;
	}
	TaViewed[t] = numOfTaViewed;


//values of the products in each TC
	for(int a=0; a<numOfTa; a++){	    
	    for(int i = 0; i<numOfFirm;i++) if((C5Model.F[i].alive == true)&&(C5Model.F[i].numOfProducts>0)){
		for(int ii=1; ii <= C5Model.F[i].numOfProducts; ii++) if(C5Model.F[i].Prod[ii].TC == a
                        && (C5Model.F[i].Prod[ii].out==false)) {
                         C5Model.TC[a].dim[t]+=C5Model.F[i].Prod[ii].historyEarnings[t];
                         C5Model.TC[a].pat[t]+=C5Model.F[i].Prod[ii].historyPatients[t];
			if (C5Model.F[i].Prod[ii].imitative==false){
			    C5Model.TC[a].existingQ[t] += (double) C5Model.F[i].Prod[ii].qp;
			}
			else C5Model.TC[a].existingQ[t] += 0;
                        C5Model.TC[a].existingQall[t] += (double) C5Model.F[i].Prod[ii].qp;
		}
	    }
            meanTaPat[t] += C5Model.TC[a].pat[t];
            meanTaDim[t] += C5Model.TC[a].dim[t];
            taDimSingle[t][a][0]=C5Model.TC[a].pat[t];
            taDimSingle[t][a][1]=C5Model.TC[a].dim[t];
	}

profitTot[t] = meanTaDim[t];
meanTaDim[t] = meanTaDim[t]/(numOfTaViewed+1);
meanTaPat[t] = meanTaPat[t]/(numOfTaViewed+1);

//Avg value of H in each TC 
	for(int i=0; i<numOfTa;i++) if(numOfTaViewed>0){
	    meanH[t]+=C5Model.TC[i].Herfindahl[t]/numOfTaViewed; 
            meanH1[t]+=C5Model.TC[i].Herfindahl1[t]/numOfTaViewed;
        }
	    
//market shares of the firms
        double tot  = 0;	
        double totPatients = 0;
	    for(int ii=0;ii< numOfFirm; ii++) if(C5Model.F[ii].alive == true){
		tot += C5Model.F[ii].totProfit;
                totPatients += C5Model.F[ii].totalReachedPatients;
	    }

	    for(int ii=0;ii< numOfFirm; ii++) if(C5Model.F[ii].alive == true){            
		if(tot == 0) C5Model.F[ii].totShare[t]=0;
		else C5Model.F[ii].totShare[t] = C5Model.F[ii].totProfit/tot;                
                if(totPatients==0) C5Model.F[ii].totShareQuantity[t]=0;
                else C5Model.F[ii].totShareQuantity[t] = C5Model.F[ii].totalReachedPatients/totPatients;
	    }
//firm size
        for(int ii=0;ii< numOfFirm; ii++) {
            if((C5Model.F[ii].alive==true)&&(C5Model.F[ii].budget>0)){
                        if (C5Model.F[ii].innovator==true)  innoSize[t]+=C5Model.F[ii].totProfit;
                        if (C5Model.F[ii].innovator==false) imiSize[t]+=C5Model.F[ii].totProfit; 
                	size[t]+=C5Model.F[ii].budget/aliveF[t];
                        if (C5Model.F[ii].innovator==true)  firmt[t][ii][0]=C5Model.F[ii].totProfit;
                        if (C5Model.F[ii].innovator==false) firmt[t][ii][1]=C5Model.F[ii].totProfit;
                        firmFeat[t][ii][0]=C5Model.F[ii].totProfit; //tot profit
                        firmFeat[t][ii][1]=C5Model.F[ii].totShare[t]; //tot share
                        firmFeat[t][ii][2]=C5Model.F[ii].numOfProducts; //tot number of products
                        firmFeat[t][ii][3]=1; //Alive
                        firmFeat[t][ii][4]=C5Model.F[ii].totalReachedPatients;
                        C5Model.F[ii].numOfTa();
                        firmFeat[t][ii][5]=C5Model.F[ii].totTC;                        
	                     }
            else firmFeat[t][ii][3]=0; //Alive
            firmFeat[t][ii][6]=C5Model.F[ii].imin;
        }
        
        if(NumInnoFirm[t]>0) innoSize[t]=innoSize[t]/NumInnoFirm[t];
        else innoSize[t]=0;
        if(NumImiFirm[t]>0) imiSize[t]=imiSize[t]/NumImiFirm[t];
        else imiSize[t]=0;

	for(int iii=0;iii<numOfTa;iii++) {
		for(int i = 0; i<numOfFirm;i++) {
		double TaFirmPos=0;
			for(int ii=1; ii <= C5Model.F[i].numOfProducts; ii++) if (C5Model.F[i].Prod[ii].TC==iii){
				TaFirmPos+=C5Model.F[i].Prod[ii].pos ;}
		}
	}

//Herfindhal
            double sumSQuantity=0;

	    for(int ii=0;ii< numOfFirm; ii++) if(C5Model.F[ii].alive == true){
		sumS += C5Model.F[ii].totShare[t];
                sumSQuantity += C5Model.F[ii].totShareQuantity[t];
	    }

            // calc Herfindhal quantity index (Total)
            for(int ii=0;ii< numOfFirm; ii++) if(C5Model.F[ii].alive == true){
		if(sumSQuantity == 0) totHQuantity[t]=0;
		else totHQuantity[t] += Math.pow((C5Model.F[ii].totShareQuantity[t]),2);//la
            }

	    // calc Herfindhal index (Total)
	    for(int ii=0;ii< numOfFirm; ii++) if(C5Model.F[ii].alive == true){
		if(sumS == 0) totH[t]=0;
		else totH[t] += Math.pow((C5Model.F[ii].totShare[t]),2);//la share usata per il calcolo di H ÃƒÂ¯Ã‚Â¿Ã‚Â½ in base alle vendite relative (vedi codice riga 2637)
	   }
            
             totFinTa[t]=0;
             totFinTainno[t]=0;
             totFinTainno[t]=0;
             boolean oneta = true;
             boolean onetainno = true;
             boolean onetaimi = true;
              for(int ii=0;ii< numOfFirm; ii++) if(C5Model.F[ii].alive == true){
                prodMeanFirm[t]+=C5Model.F[ii].numOfProducts/aliveF[t];
                 for(int tac=0;tac<C5Model.numOfTC; tac++){
                    oneta=false;
                    onetaimi=false;
                    onetainno=false;
                    for(int pp=1; pp<= C5Model.F[ii].numOfProducts; pp++){
                       if(C5Model.F[ii].Prod[pp].TC ==tac && C5Model.F[ii].Prod[pp].out==false && oneta==false){
                         totFinTa[t]++;
                         tat[t][tac][0]++;
                         oneta=true;
                       }
                       if(C5Model.F[ii].Prod[pp].TC ==tac && 
                               C5Model.F[ii].Prod[pp].out==false && onetainno==false
                                    && C5Model.F[ii].innovator==true){
                         totFinTainno[t]++;
                           tat[t][tac][2]++;
                         onetainno=true;
                       }
                       if(C5Model.F[ii].Prod[pp].TC ==tac && 
                               C5Model.F[ii].Prod[pp].out==false && onetaimi==false
                                && C5Model.F[ii].innovator==false){
                           totFinTaimi[t]++;
                         tat[t][tac][3]++;
                         onetaimi=true;
                       }
                       if(C5Model.F[ii].Prod[pp].TC == tac){
                          tat[t][tac][1]++;
                                                          }
                    }
                  }
                 }
             if(TaViewed[t]!=0)  meanFTA[t]=totFinTa[t]/(TaViewed[t]);
             else meanFTA[t]=0;
              if(TaViewed[t]!=0) meanFTAinno[t]=totFinTainno[t]/(TaViewed[t]);
              else meanFTAinno[t]=0;
               if(TaViewed[t]!=0)meanFTAimi[t]=totFinTaimi[t]/(TaViewed[t]);
               else meanFTAimi[t]=0;
            
double leader2=0;

for(int ii=0;ii<C5Model.numOfFirm; ii++)
    if((C5Model.F[ii].alive == true) &&(C5Model.F[ii].numOfProducts>0)){
        if (C5Model.F[ii].totShare[t] >= leader2) {
			leader2 = C5Model.F[ii].totShare[t];
			firmLeader[t] = ii;
	          }

	}

if(t>1)
if (firmLeader[t]!=firmLeader[t-1]) {
 leaderStability[t]=C5Model.stab;
 C5Model.stab=C5Model.stab+1;
 }
else leaderStability[t]=leaderStability[t-1];

//r&d sales
for(int ii=0;ii<C5Model.numOfFirm; ii++)
    if((C5Model.F[ii].alive == true) &&(C5Model.F[ii].numOfProducts>0)){
			redsales[t] += ((C5Model.F[ii].search_research)/aliveFwithProd[t]);
                        redsales1[t] += ((C5Model.F[ii].search_research)/aliveFwithProd[t])*C5Model.F[ii].totShare[t];
	}


multiTotH[t]                    += totH[t]/multiTime;
multiTotHQuantity[t]            += totHQuantity[t]/multiTime;
multiTaDim[t]                   += meanTaDim[t]/multiTime;
multiTaPat[t]                   += meanTaPat[t]/multiTime;
multiPrTot[t]                   += profitTot[t]/multiTime;
multiOutProd[t]                 += outProd[t]/multiTime;
multiAliveF[t]			+= aliveF[t] / multiTime;
multiAliveFwithProd[t]		+= aliveFwithProd[t] / multiTime;
multiInnoNature[t]              += innoNature[t]/multiTime;
multiImiNature[t]               += imiNature[t]/multiTime;
multiInnoNumber[t]              += innoNumber[t] /multiTime;
multiImiNumber[t]               += imiNumber[t] /multiTime;
multiPrice[t]                   += priceMean[t];
multiPriceInno[t]               += priceMeanInno[t];
multiPriceImi[t]                += priceMeanImi[t];
multiG[t]                       += g[t];
multiGInno[t]                   += gInno[t];
multiGImi[t]                    += gImi[t];
multiCount[t]                   += countSVIL[t];
multiCountInno[t]               += countSvilInno[t];
multiCountImi[t]                += countSvilImi[t];
multiAliveIncumbentFirm[t]	+= aliveIncumbentFirm[t] / multiTime;
multiAliveNBF[t]		+= aliveNBF[t] / multiTime;
multiNumInnoFirm[t]		+= NumInnoFirm[t] / multiTime;
multiTaViewed[t]		+= TaViewed[t] /multiTime;
multiMeanH[t]		        += meanH[t]/multiTime;
multiMeanH1[t]                  += meanH1[t]/multiTime;
multiSize[t]		        += size[t]/multiTime;
multiLeaderStability[t]         += leaderStability[t]/multiTime;
multiredsales[t]         += redsales[t]/multiTime;
multiredsales1[t]         += redsales1[t]/multiTime;
multiInnoSize[t]                += innoSize[t]/multiTime; 
multiImiSize[t]                 += imiSize[t]/multiTime; 
multiSizeInc[t]		        += sizeInc[t]/multiTime;
multiSizeNBF[t]		        += sizeNBF[t]/multiTime;
multiInnoProd[t]	        += innoProd[t]/ multiTime;
multiQInno[t]                   += qInno[t]/multiTime;
multiImiProd[t]		        += imiProd[t]/ multiTime;
}

//parameters "parameters.txt"
     public static void reportXls(int endTime, int numOfFirm, int numOfTa) {
	    C5Model.FILE.printParam("Multi Time: "+C5Model.mt+"\n");
            C5Model.FILE.printParam("drawCost: "+C5Model.drawCost+"\n");         
            C5Model.FILE.printParam("numOfFirm: "+C5Model.numOfFirm+"\n");         
            C5Model.FILE.printParam("numOfTC: "+C5Model.numOfTC+"\n");         
            C5Model.FILE.printParam("TCValueCost: "+C5Model.TCPatientsCost+"\n");         
            C5Model.FILE.printParam("numOfMol: "+C5Model.numOfMol+"\n");         
            C5Model.FILE.printParam("qMolNull: "+C5Model.qMolNull+"\n");         
            C5Model.FILE.printParam("patentDuration: "+C5Model.patentDuration+"\n");                     
            C5Model.FILE.printParam("CostOfSearch: "+C5Model.costOfSearch+"\n");         
            C5Model.FILE.printParam("costOfResearchInn: "+C5Model.costOfResearchInn+"\n");         
	    C5Model.FILE.printParam("costOfResearchImi: "+C5Model.costOfResearchImi+"\n");
            C5Model.FILE.printParam("Initial Budget: "+C5Model.B+"\n");         
            C5Model.FILE.printParam("qualityCheck: "+C5Model.qualityCheck+"\n");                          
            C5Model.FILE.printParam("AvgWeightInno: "+C5Model.speedDevelopmentInno+"\n");         
            C5Model.FILE.printParam("AvgWeightImi: "+C5Model.speedDevelopmentImi+"\n");         
            C5Model.FILE.printParam("Product exits below this threshold: "+C5Model.outProLimit+"\n");         
            C5Model.FILE.printParam("Firm exits market after n unsuccesful searches: "+C5Model.searchFailure+"\n");                           
            C5Model.FILE.printParam("interestRate: "+C5Model.interestRate+"\n");                    
	    C5Model.FILE.printParam("timeDevelop: "+C5Model.timeDevelop+"\n");
            C5Model.FILE.printParam("erosion marketing: "+C5Model.erosion+"\n");         
            C5Model.FILE.printParam("Firm exits below this threshold: "+C5Model.eFailure+"\n");         
            C5Model.FILE.printParam("costProd: "+C5Model.costProd+"\n");         
            C5Model.FILE.printParam("eta: "+C5Model.omega+"\n");         
            C5Model.FILE.printParam("elasticity in the markup formula: "+C5Model.elasticity+"\n");                                 
            C5Model.FILE.printParam("endTime: "+C5Model.endTime+"\n");         
            C5Model.FILE.printParam("patentOriz: "+C5Model.patentWidth+"\n");         
            C5Model.FILE.printParam("TCValueRand: "+C5Model.TCPatientsRand+"\n");         
            C5Model.FILE.printParam("a avg: "+C5Model.aValueCost+"\n");
            C5Model.FILE.printParam("a range: "+C5Model.aValueRand+"\n");         
            C5Model.FILE.printParam("b avg: "+C5Model.bValueCost+"\n");         
            C5Model.FILE.printParam("b range: "+C5Model.bValueRand+"\n");         
            C5Model.FILE.printParam("c avg: "+C5Model.cValueCost+"\n");         
            C5Model.FILE.printParam("c range: "+C5Model.cValueRand+"\n");         
            C5Model.FILE.printParam("qMolCost: "+C5Model.qMolCost+"\n");         
            C5Model.FILE.printParam("qMolVar: "+C5Model.qMolVar+"\n");         
            C5Model.FILE.printParam("numOfSubMKT: "+C5Model.numOfSubMKT+"\n");         
            C5Model.FILE.printParam("% of R&D budget invested in search: "+C5Model.quotaInvestedInSearch+"\n");      

//ouput statistics "multiout.txt"          
C5Model.FILE.print("H,H_avg_TC,prod_inno,prod_imi,alive_firms_with_prod,TC_viewed,price_inno,price_imi"+"\n");
 for(int t=1; t<= endTime; t++){
	    C5Model.FILE.print(multiTotH[t] + ",");         
            C5Model.FILE.print(multiMeanH[t] + ",");       
            C5Model.FILE.print(multiInnoProd[t] + ",");    
            C5Model.FILE.print(multiImiProd[t] + ",");                 
            C5Model.FILE.print(multiAliveFwithProd[t] + ",");    
            C5Model.FILE.print(multiTaViewed[t] + ",");    
            if (zeros[t][6] < C5Model.mt) {
                C5Model.FILE.print(multiPriceInno[t] / (C5Model.mt - zeros[t][6]) + ",");   
            } else {
                C5Model.FILE.print(multiPriceInno[t] / (C5Model.mt) + ",");
            }
            if (zeros[t][7] < C5Model.mt) {
                C5Model.FILE.print(multiPriceImi[t] / (C5Model.mt - zeros[t][7]) + "");  
            } else {
                C5Model.FILE.print(multiPriceImi[t] / (C5Model.mt) + "");
            }           
            C5Model.FILE.print("\n");
        }	
     }
}

final class files {

    static DataOutputStream fp,fparam;

    public files() {

    }      
    public static void createDir(String dirName){

      try{
    boolean success = (new File(dirName)).mkdirs();
    if (success) {System.out.println("Directory: " + dirName + " created");
    }

    }catch (Exception e){System.err.println("Error: " + e.getMessage());
    }
}

     public static void print(String str) {
	try {fp.writeBytes(str);} catch (IOException e) {System.out.println(e.getMessage());}
    }

  public static void printParam(String str) {
	try {fparam.writeBytes(str);} catch (IOException e) {System.out.println(e.getMessage());}
    }

     public static void initFiles(String name) { 
         try {
		fp = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(name+"/multiout.txt")));
	    }
	    catch (IOException e) {
		System.out.println(e.getMessage());
	    }

          try {
		fparam = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(name+"/param.txt")));
	    }
	    catch (IOException e) {
		System.out.println(e.getMessage());
	    }
    }



     public static void closeFiles() { 
        try {
          fp.flush();
	  fp.close();
	}
	catch (IOException e) {
	  System.out.println(e.getMessage());
	}

         try {
	  fparam.flush();
	  fparam.close();
	}
	catch (IOException e) {
	  System.out.println(e.getMessage());
	}
    }

}

