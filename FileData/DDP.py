def DDP(multiplier, modifier_density, target_dist, target_density):

        # amount of modifier density values that remains to
        # be matched up with the target distribution
        modifier_count = 0

        # amount of target density values that remains to be
        # matched up with the multiplier distribution
        target_count = 0

        # new distribution to be created
        new_dist = []           

        # gets first multiplier element
        multiplier_value = multiplier.next()

        # gets first modifier_density element
        modifier_count = modifier_density.next()
        
        # iterates through each of the target_density values 
        for target_density_value in target_density:

            # stores information to create the a new distirbution value
            store = []  

            # keeps track of remaining amount of target_density values unaccounted for
            target_count += target_density_value
                        
            # case where there is more target_density values unaccounted for
            while(target_count > modifier_count):
                store.append((modifier_count, multiplier_value))            
                target_count -= modifier_count      
                            
                if multiplier.hasNext() and modifier_density.hasNext():
                    # gets next multiplier value
                    multiplier_value = multiplier.next()
                    # gets next modifier_density value
                    modifier_count = modifier_density.next()
                
            
            # case where there is more modifier density values unaccounted for
            if (target_count <= modifier_count):
                store.append((target_count, multiplier_value))
                modifier_count -= target_count
                target_count = 0.0
                
            # produces a new value for the adjusted modifier distribution
            total_count = 0
            total_val = 0
            
            for count, val in store:
                # using a weighted average
                total_count += count
                total_val += count*val
                
            if total_count:
                # normalizing the weighted average
                total_val /= total_count
            else:
                total_val = 0

            # gets next value from the target distribution
            target_dist_value = target_dist.next()

            # adds the new value to the new distribution       
            new_dist.append(total_val * target_dist_value)


        # returns new distribution
        return new_dist
                    
            
