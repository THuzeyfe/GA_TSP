from RouteManager import RouteManager
from Route import Route

import numpy as np


class GeneticAlgorithmSolver:
    def __init__(self, cities, population_size=50, mutation_rate=0.05, tournament_size=5, elitism=True):
        self.cities = cities
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.elitism = elitism

    def solve(self, rm):
        rm = self.evolve(rm)
        for i in range(100):
            rm = self.evolve(rm)
        return rm

    def evolve(self, routes):
        '''This function provides general flow to create a new generation
        from given population
        Input:
            routes: RouteManager object that will be evolved
        Output:
            child: new generation of RouteManager
        '''
        selected_routes = RouteManager(self.cities,self.population_size) #to store routes in selection state
        
        #SELECTION STATE
        for i in range(self.population_size-int(self.elitism)):
            #replace existing routes with tournament winners
            #as many as tournament_size particapants are chosen randomly
            selected_routes.set_route(i, self.tournament(np.random.choice(routes.routes, self.tournament_size)))

        
        ##ELITISM PART
        child_routes = RouteManager(self.cities,self.population_size) #to store new child routes
        if self.elitism: #if elitism then best route will directly pass to next generation
            temporary_route = Route(self.cities)
            elite_route = routes.find_best_route()
            for i in range(len(elite_route)):
                temporary_route.assign_city(i,elite_route.get_city(i))
            child_routes.set_route(self.population_size-1, temporary_route)

        #CROSS-OVER STATE
        for i in range(self.population_size-int(self.elitism)):
            #replace existing child routes with actually generated ones
            #first route is matched with last, second is matched with second from last and so on.
            child_routes.set_route(i, self.crossover(selected_routes.get_route(i),selected_routes.get_route(self.population_size-1-i)))

        #MUTATION STATE
        for i in range(len(child_routes)-int(self.elitism)):
            #send each routes to mutation function
            self.mutate(child_routes.get_route(i))
        
        return child_routes

    def crossover(self, route_1, route_2):
        '''This function creates a crossed-over child route from
        two given parent routes.
        Input:
            route_1: first parent route
            route_2: second parent route
        Output:
            child: generated child route
        '''
        #determining random start and end genes 
        #which will stay same as in the first parent
        a = np.random.rand()
        b = np.random.rand()
        low_point=int(min(a,b)*len(self.cities))
        up_point=int(max(a,b)*len(self.cities))
        
        child=route_1 #child creation
        gen_list=[] #this list stores the cities as in the generated child's order
        for i in range(low_point,up_point):
            #from randomly generated low to up point cities will stay same
            gen_list.append(route_1.get_city(i))
        
        #subset contains cities that hasnot been added to gen list and as in the second parent's order 
        subset=[item for item in route_2.route if item not in gen_list]
        
        #add the cities in the subset
        for i in range(len(self.cities)):
            if i not in range(low_point,up_point):
                indx=i if i<low_point else i-(up_point-low_point)
                child.assign_city(i,subset[indx])
        
        return child

    def mutate(self, route):
        '''This function randomly deformate the genes with
        a given probabiliy
        Input:
            route: RouteManager object that would mutate
        Output:
            None
        '''
        for i in range(len(route)): #each gene can be subject to mutation
            if np.random.rand()<self.mutation_rate: #mutation occurs with the probality of mutation_rate
                #if probabability occurs given gene is replaced with another random gene
                swap_indx=int(len(route)*np.random.rand())
                city1 = route.get_city(i)
                city2 = route.get_city(swap_indx)
                route.assign_city(i,city2)
                route.assign_city(swap_indx, city1)

        return

    def tournament(self, routes):
        '''This function returns the route with best fitness score
        among a set of routes.
        Input:
            routes: list of routes
        Output:
            return_route: route that gives best fitness
        '''
        best_fitness=0 #first set
        for r in routes:
            if r.calc_fitness()>best_fitness: #update if better route exist than current best.
                best_fitness=r.calc_fitness()
                tour_winner=r
                
        return_route = Route(self.cities) #creating the return value
        for i in range(len(return_route)):
            return_route.assign_city(i,tour_winner.get_city(i))
           
        return return_route