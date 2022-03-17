class Print_Result:

    #converts 0/1 format to required format    
    def convert_to_printable(model):
        return [i+1 if model[i] else -(i+1) for i in range(len(model))]

    #prints output to console
    def print_result(sentence, best_model, fitness_value, time):
            
            best_model_printable = Print_Result.convert_to_printable(best_model)

            print("\n\n")
            print("Roll No : 2019A7PS0032G")
            print("Number of clauses in CSV file :",len(sentence))
            print("Best model :", best_model)
            print("Fitness value of best model :", fitness_value, end="%\n")
            print("Time taken : {:.2f} seconds".format(time))
            print("\n\n")
