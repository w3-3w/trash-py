"""
Cookie Clicker Simulator
"""

import simpleplot

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided
import math

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._cookies = 0.0
        self._cps = 1.0
        self._time = 0.0
        self._total = 0.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        status_repr = "total: " + str(self.get_total()) + "\n  now: "
        status_repr += str(self.get_cookies()) + "\n time: " + str(self.get_time())
        status_repr += "\n  CPS: " + str(self.get_cps()) + "\n"
        return status_repr
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time
    
    def get_history(self):
        """
        Return history list
        """
        return self._history

    def get_total(self):
        """
        Return total number of cookies
        """
        return self._total
    
    def add_cookies(self, cookies):
        """
        Add the number of current cookies and total number
        of cookies
        """
        self._cookies += cookies
        self._total += cookies
        
    def operate_buy(self, cost, cps):
        """
        Charge cookies and add CPS
        """
        self._cps += cps
        self._cookies -= cost
        
    def add_time(self, time):
        """
        Add current time
        """
        self._time += time
        
    def append_history(self, history_item):
        """
        Add history to history list
        """
        self._history.append(history_item)

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if (self.get_cookies() >= cookies):
            return 0.0
        else:
            return math.ceil((cookies - self.get_cookies()) / self.get_cps())
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if (time >= 0):
            cookies_earned = time * self.get_cps()
            self.add_time(time)
            self.add_cookies(cookies_earned)
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if (self.get_cookies() >= cost):
            self.operate_buy(cost, additional_cps)
            self.append_history((self.get_time(), item_name, cost, self.get_total()))
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    ava_builds = build_info.clone()
    clicker = ClickerState()
    while (clicker.get_time() <= duration):
        item = strategy(clicker.get_cookies(), clicker.get_cps(),
                        duration - clicker.get_time(), ava_builds)
        if (item):
            cost = ava_builds.get_cost(item)
            next_time = clicker.time_until(cost)
            if (next_time + clicker.get_time() > duration):
                break
            clicker.wait(next_time)
            ava_builds.update_item(item)
            clicker.buy_item(item, cost, ava_builds.get_cps(item))
        else:
            break
    clicker.wait(duration - clicker.get_time())
    return clicker


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    Returns the cheapest item in buildable list.
    """
    cost = float("inf")
    choice = None
    for item in build_info.build_items():
        if (build_info.get_cost(item) < cost):
            temp_cost = build_info.get_cost(item)
            if (time_left >= (temp_cost - cookies) / cps):
                cost = temp_cost
                choice = item
    return choice

def strategy_expensive(cookies, cps, time_left, build_info):
    """
    Returns the most expensive item in buildable list.
    """
    cost = float("-inf")
    choice = None
    for item in build_info.build_items():
        if (build_info.get_cost(item) > cost):
            temp_cost = build_info.get_cost(item)
            if (time_left >= (temp_cost - cookies) / cps):
                cost = temp_cost
                choice = item
    return choice

def strategy_best(cookies, cps, time_left, build_info):
    """
    Returns the best choice.
    """
    ratio = 0
    choice = None
    for item in build_info.build_items():
        ratio_to_compare = build_info.get_cps(item) / build_info.get_cost(item)
        if (ratio_to_compare > ratio):
            temp_cost = build_info.get_cost(item)
            if (time_left >= (temp_cost - cookies) / cps):
                ratio = ratio_to_compare
                choice = item
    return choice
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":\n", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor)
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
run()
