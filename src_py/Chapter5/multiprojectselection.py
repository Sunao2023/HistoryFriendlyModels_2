#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MultiProjectSelection class for the pharmaceutical industry model.
This class contains methods to select the most promising research projects.
"""

class MultiProjectSelection:
    """
    Class to manage project selection for firms.
    
    This class implements algorithms for selecting the most promising
    research projects based on their expected value and available budget.
    """
    
    @staticmethod
    def in_vet(vet_ta, vet_mol, ta, mol):
        """
        Check if a molecule is in the vector of molecules.
        
        Args:
            vet_ta (list): List of therapeutic categories
            vet_mol (list): List of molecules
            ta (int): Therapeutic category to check
            mol (int): Molecule ID to check
            
        Returns:
            bool: True if the molecule is in the vector, False otherwise
        """
        for v in range(len(vet_ta)):
            if vet_mol[v] == mol and vet_ta[v] == ta:
                return True
        return False
    
    @staticmethod
    def order_value(val, cap, f, t, model):
        """
        Order project values and select the most promising ones.
        
        Args:
            val (list): List of values
            cap (int): Capacity (how many projects to select)
            f (int): Firm ID
            t (int): Current time period
            model: C5Model instance
        """
        # For each potential project
        for count in range(cap):
            pos_best = -1
            c = 0
            ta = [0] * model.num_of_tc
            
            # If the firm is innovative
            if model.f[f].innovatort:
                vtot = 0.0
                
                # Calculate total value for normalization
                for i in range(len(model.f[f].on_pro_inno.mem_of_tc)):
                    # Skip if index out of range
                    if i >= len(model.f[f].on_pro_inno.on) or model.f[f].on_pro_inno.on[i] != 0:
                        continue
                        
                    # Check if TC and molecule indices are valid
                    tc_id = model.f[f].on_pro_inno.mem_of_tc[i]
                    if tc_id >= len(model.tc) or model.tc[tc_id] is None:
                        continue
                        
                    mol_id = model.f[f].on_pro_inno.mem_of_mol[i]
                    if mol_id >= len(model.tc[tc_id].mol) or model.tc[tc_id].mol[mol_id] is None:
                        continue
                    
                    # Calculate patent time multiplier
                    patent_time = model.tc[tc_id].mol[mol_id].patent_time
                    
                    multiplier = (model.patent_duration - (t - patent_time)) / model.patent_duration
                    
                    # Only count if firm owns the patent or multiplier is positive
                    if model.tc[tc_id].mol[mol_id].patent_by == f and multiplier > 0:
                        pass  # Keep multiplier as is
                    else:
                        multiplier = 0
                    
                    # Add to total value (equation 4 in chapter 5)
                    if i < len(model.f[f].on_pro_inno.value):
                        vtot += model.f[f].on_pro_inno.value[i] * multiplier
                        c += 1
                        if tc_id < len(ta):
                            ta[tc_id] += 1
                
                # If there are available projects
                if c > 0:
                    casual = model.r.random()
                    ti = 0.0
                    exit_flag = False
                    
                    # Select project with probability proportional to value
                    for i in range(len(model.f[f].on_pro_inno.mem_of_tc)):
                        # Skip if index out of range
                        if i >= len(model.f[f].on_pro_inno.on) or model.f[f].on_pro_inno.on[i] != 0 or exit_flag:
                            continue
                            
                        # Check if TC and molecule indices are valid
                        tc_id = model.f[f].on_pro_inno.mem_of_tc[i]
                        if tc_id >= len(model.tc) or model.tc[tc_id] is None:
                            continue
                            
                        mol_id = model.f[f].on_pro_inno.mem_of_mol[i]
                        if mol_id >= len(model.tc[tc_id].mol) or model.tc[tc_id].mol[mol_id] is None:
                            continue
                        
                        patent_time = model.tc[tc_id].mol[mol_id].patent_time
                        
                        multiplier = (model.patent_duration - (t - patent_time)) / model.patent_duration
                        
                        if model.tc[tc_id].mol[mol_id].patent_by == f and multiplier > 0:
                            pass  # Keep multiplier as is
                        else:
                            multiplier = 0
                        
                        # Calculate probability based on value
                        if vtot > 0 and i < len(model.f[f].on_pro_inno.value):
                            ti += (model.f[f].on_pro_inno.value[i] * multiplier / vtot)
                        
                        if not exit_flag and ti > casual:
                            exit_flag = True
                            pos_best = model.f[f].select_mol(ta, i, model.f[f].on_pro_inno)
                
                # If a project was selected, mark it as active
                if pos_best != -1 and pos_best < len(model.f[f].on_pro_inno.on):
                    model.f[f].on_pro_inno.on[pos_best] = 1
                    tc_id = model.f[f].on_pro_inno.mem_of_tc[pos_best]
                    mol_id = model.f[f].on_pro_inno.mem_of_mol[pos_best]
                    
                    # Ensure TC and molecule indices are valid before incrementing counters
                    if tc_id < len(model.tc) and model.tc[tc_id] is not None:
                        if mol_id < len(model.tc[tc_id].mol) and model.tc[tc_id].mol[mol_id] is not None:
                            model.tc[tc_id].mol[mol_id].on_mol_res += 1
                            model.tc[tc_id].on_ta_res += 1
            
            # If the firm is imitative
            else:
                vtot = 0.0
                
                # Calculate total value for normalization
                for i in range(len(model.f[f].on_pro_imi.mem_of_tc)):
                    # Skip if index out of range or already in development
                    if (i >= len(model.f[f].on_pro_imi.on) or 
                        model.f[f].on_pro_imi.on[i] != 0):
                        continue
                    
                    # Skip if already being researched innovatively
                    tc_id = model.f[f].on_pro_imi.mem_of_tc[i] if i < len(model.f[f].on_pro_imi.mem_of_tc) else -1
                    mol_id = model.f[f].on_pro_imi.mem_of_mol[i] if i < len(model.f[f].on_pro_imi.mem_of_mol) else -1
                    
                    if tc_id == -1 or mol_id == -1:
                        continue
                    
                    # Check if already in innovative portfolio
                    if MultiProjectSelection.in_vet(
                        model.f[f].on_pro_inno.mem_of_tc,
                        model.f[f].on_pro_inno.mem_of_mol,
                        tc_id, mol_id):
                        continue
                    
                    # Add to total value
                    if i < len(model.f[f].on_pro_imi.value):
                        vtot += model.f[f].on_pro_imi.value[i]
                        c += 1
                        if tc_id < len(ta):
                            ta[tc_id] += 1
                
                # If there are available projects
                if c > 0:
                    casual = model.r.random()
                    ti = 0.0
                    exit_flag = False
                    
                    # Select project with probability proportional to value
                    for i in range(len(model.f[f].on_pro_imi.mem_of_tc)):
                        # Skip if index out of range, already in development, or already selected
                        if (i >= len(model.f[f].on_pro_imi.on) or 
                            model.f[f].on_pro_imi.on[i] != 0 or 
                            exit_flag):
                            continue
                        
                        # Skip if already being researched innovatively
                        tc_id = model.f[f].on_pro_imi.mem_of_tc[i] if i < len(model.f[f].on_pro_imi.mem_of_tc) else -1
                        mol_id = model.f[f].on_pro_imi.mem_of_mol[i] if i < len(model.f[f].on_pro_imi.mem_of_mol) else -1
                        
                        if tc_id == -1 or mol_id == -1:
                            continue
                        
                        # Check if already in innovative portfolio
                        if MultiProjectSelection.in_vet(
                            model.f[f].on_pro_inno.mem_of_tc,
                            model.f[f].on_pro_inno.mem_of_mol,
                            tc_id, mol_id):
                            continue
                        
                        # Calculate probability based on value
                        if vtot > 0 and i < len(model.f[f].on_pro_imi.value):
                            ti += (model.f[f].on_pro_imi.value[i] / vtot)
                        
                        if not exit_flag and ti > casual:
                            exit_flag = True
                            pos_best = model.f[f].select_mol(ta, i, model.f[f].on_pro_imi)
                
                # If a project was selected, mark it as active
                if pos_best != -1 and pos_best < len(model.f[f].on_pro_imi.on):
                    model.f[f].on_pro_imi.on[pos_best] = 1
                    
                    # Get TC and molecule IDs
                    tc_id = model.f[f].on_pro_imi.mem_of_tc[pos_best] if pos_best < len(model.f[f].on_pro_imi.mem_of_tc) else -1
                    mol_id = model.f[f].on_pro_imi.mem_of_mol[pos_best] if pos_best < len(model.f[f].on_pro_imi.mem_of_mol) else -1
                    
                    # Ensure TC and molecule indices are valid before incrementing counters
                    if tc_id != -1 and tc_id < len(model.tc) and model.tc[tc_id] is not None:
                        if mol_id != -1 and mol_id < len(model.tc[tc_id].mol) and model.tc[tc_id].mol[mol_id] is not None:
                            model.tc[tc_id].mol[mol_id].on_mol_res += 1
                            model.tc[tc_id].on_ta_res += 1
    
    @staticmethod
    def in_projects(weights, values, capacity, f, t, model):
        """
        Select projects to pursue based on budget constraints.
        
        Args:
            weights (list): Cost weights of projects
            values (list): Values of projects
            capacity (int): Maximum number of projects (budget capacity)
            f (int): Firm ID
            t (int): Current time period
            model: C5Model instance
        """
        # If no capacity, return
        if capacity <= 0:
            return
            
        # Order projects by value and select the best ones
        MultiProjectSelection.order_value(values, capacity, f, t, model) 