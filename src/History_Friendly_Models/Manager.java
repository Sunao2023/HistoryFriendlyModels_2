/* ACKNOWLEDGMENTS
 * Chapter 3 model features the Binomial distribution included in the JSC     *
 * library (© Andrew James Bertie, 2004), that is not included in this        *
 * distributon, but can be downloaded from the following website              *
 * http://www.jsc.nildram.co.uk/                                              */

package History_Friendly_Models;

import Chapter3.C3Model;
import Chapter4.C4Model;
import Chapter5.C5Model;

/*                                                                            *
 * Innovation and the Evolution of Industries. History Friendly Models:       *
 * Simulation code                                                            *
 * @author Gianluca Capone & Davide Sgobba                                    *
 *                                                                            */

public class Manager {

    public static void main(String[] args) {
    /* This is the code to reproduce the data of Chapter 3. To run the code,  *
     * remove the "//" from the beginning of one of the lines. Put back the   *
     * "//" at the beginning if you want to switch to a different type of     *
     * simulation or to another model                                         */
       C3Model model_ch3 = new C3Model();
    /* The first line runs a single simulation and saves results in the file  *
     * "simulation.csv"                                                       */
        model_ch3.makeSingleSimulation(true);
    /* The second line runs a multiple simulation and saves results in the    *
     * file "simulation.csv"                                                  */
        model_ch3.makeMultipleSimulation(true);
    /* The third line runs sensitivity analysis and saves results in multiple *
     * filea named after the corresponding statistic                          */
        model_ch3.makeSensitivitySimulation(true);
        
    /* This is the code to reproduce the data of Chapter 4. To run the code,  *
     * remove the "//" from the beginning of one of the lines. Put back the   *
     * "//" at the beginning if you want to switch to a different type of     *
     * simulation or to another model                                         */
        C4Model model_ch4 = new C4Model();
    /* The first line runs a single simulation and saves results in the file  *
     * "singleSimulation.csv"                                                 */
        //model_ch4.makeSingleSimulation(true);
    /* The second line runs a multiple simulation and saves results in the    *
     * file "multiSimulation.csv"                                             */
        //model_ch4.makeMultipleSimulation(true);
    /* The third line runs sensitivity analysis and saves results in multiple *
     * filea named after the corresponding statistic                          */
        //model_ch4.makeSensitivitySimulation(true);
    
    /* This is the code to reproduce the data of Chapter 5. To run the code,  *
     * remove the "//" from the beginning of one of the lines. Put back the   *
     * "//" at the beginning if you want to switch to a different type of     *
     * simulation or to another model                                         */
        C5Model model_ch5 = new C5Model();
    /* The first line runs a single simulation and saves results in the file  *
     * "multiout.txt" and the parameters used in the file "param.txt"         */
        //model_ch5.makeSingleSimulation();
    /* The second line runs a multiple simulation and saves results in the    *
     * file "multiout.txt" and the parameters used in the file "param.txt"    */
        //model_ch5.makeMultipleSimulation();
    }
}
