/*
 *
 * Author ~ Andrew Meinke
 *
 * Statistics C library for common statistical functions
 * 
 * Contains
 *  - An object that will hold statistical data and a 1D dataset
 *  - Functions to compute:
 *      mean
 *      variance
 *  - Supporting functions:
 *      Copy data into Dataset object's variable length data member
 *
 */

#ifndef statistics_H
#define statistics_H

    #include <stdio.h>
    #include <stdlib.h>
    #include <errno.h>
    #include <string.h>

    #ifndef pabort_F
    #define pabort_F
        static void pabort(const char *s) {
            perror(s);
            abort();
        } // stdlib.h, errno.h
    #endif /* pabort */

    #ifndef lenof_F
    #define lenof_F
        #define lenof(a) ( sizeof(a) / sizeof(a[0]) )
    #endif /* lenof_F */

    struct sDataset {
        int len;
        float mean;
        float var;
        float * data;
    };

    // Calculates mean of Data
    float mean(int n, float data[]) {
        float mean = 0;
        
        for(int i=0; i<n; i++) {
            mean += data[i];
        }
        mean /= n;
        return mean;
    }// none
    
    // Calculates Variance of Data
    double var(int n, float mean, float * data) {
        float var = 0;
        float x = 0;
        
        // Preform Variance
        for(int i=0; i<n; i++) {
            x = data[i]-mean; // (xi - mean)
            var += x*x; // (xi - mean)^2
        }
        var /= (n-1); // (xi - mean)^2 / (n-1)
        
        return var;
    }// none
    
    struct sDataset createDataset(int n, float * fpData) {
        // Copy given info into dataset
        float * spTarget = (float*) malloc(n*sizeof(float));
        if (spTarget == 0) pabort("ERROR: Out of memory\n");
        memcpy((spTarget), fpData, n*sizeof(float));
        
        struct sDataset set = {.len=n, .data=spTarget};
        set.mean = mean(set.len, set.data);
        set.var = var(set.len, set.mean, set.data);
        
        return set;
    }// stdlib.h
    
    // Zeros out Dataset's statistics and deletes the Dataset's data
    void deleteDataset(struct sDataset * set) {
        set->len = 0;
        free(set->data);
        set->mean = 0;
        set->var = 0;
        return;
    }// stdlib.h
    
    // Prints a line with nlen number of dashes
    static void printDashLine(int nlen) {
        for(int i=0; i<nlen; ++i) {
            printf("-");
        }
        printf("\n");
        return;
    }// stdio.h
    
    void printInfo(struct sDataset * spSet) {
        puts("Data's Statistics");
        printDashLine(30);
        printf("  leng : %d\n", spSet->len);
        printf("  mean : %f\n", spSet->mean);
        printf("  vari : %f\n", spSet->var);
        puts("");
        return;
    }// stdio.h
    
    void printData(struct sDataset * spSet, int Wrap) {
        puts("Data");
        printDashLine(30);
        for(int I=0; I<(spSet->len); I++) {
            printf(" %f", spSet->data[I]);
            if((Wrap !=0) && ((I+1)%Wrap==0)) {printf("\n");}
        }
        puts("");
    }// stdio.h
    // Wrapping is provided for printing large datasets to smaller screens
    
#endif /* statistics_H */
    
    
    
/* Example use code

#include <stdio.h>
#include "statistics.h"
#include "statistics.h"

int main()
{
    float *pd, d[4] = {10.65,33.4554,54.646,46.46};
    pd = &d[0];
    
    // Create new Dataset
    struct sDataset Set1 = createDataset(lenof(d), d), *pSet1 = &Set1;
    pSet1 = &Set1;
    
    // Print Struct
    printInfo(pSet1);
    printData(pSet1, 5);
    
    puts("");
    
    // Delete Dataset
    deleteDataset(pSet1);
    // Print Struct
    printInfo(pSet1);
    printData(pSet1, 5);

    return 0;
}
*/
