import random
import simpy
import statistics
import matplotlib.pyplot as plt

class SupermarketCheckoutSystem:
    def __init__(self, env, num_checkout_lanes, arrival_rate, items_per_customer, service_rate):
        self.env = env
        self.checkout_lanes = simpy.Resource(env, capacity=num_checkout_lanes)
        self.arrival_rate = arrival_rate
        self.items_per_customer = items_per_customer
        self.service_rate = service_rate
        self.waiting_times = []

    def customer(self, customer_id):
        arrival_time = self.env.now
        print(f"Customer {customer_id} arrives at time {arrival_time}")

        with self.checkout_lanes.request() as request:
            yield request

            service_start_time = self.env.now
            print(f"Customer {customer_id} starts checkout at time {service_start_time}")

            items_scanned_time = self.items_per_customer * random.uniform(0.8, 1.2)
            yield self.env.timeout(items_scanned_time)

            service_end_time = self.env.now
            print(f"Customer {customer_id} finishes checkout at time {service_end_time}")

            waiting_time = service_start_time - arrival_time
            self.waiting_times.append(waiting_time)

    def run_simulation(self, num_customers):
        for customer_id in range(num_customers):
            self.env.process(self.customer(customer_id))
            inter_arrival_time = random.expovariate(self.arrival_rate)
            yield self.env.timeout(inter_arrival_time)

def main():
    num_checkout_lanes = 2
    arrival_rate = 0.5  # Customers per minute
    items_per_customer = 5
    service_rate = 1.0  # Items per minute
    num_customers = 10

    env = simpy.Environment()
    supermarket = SupermarketCheckoutSystem(env, num_checkout_lanes, arrival_rate, items_per_customer, service_rate)
    env.process(supermarket.run_simulation(num_customers))
    env.run()

    # Calculate and print statistics
    avg_waiting_time = statistics.mean(supermarket.waiting_times)
    print(f"\nAverage Waiting Time: {avg_waiting_time:.2f} minutes")

    # Visualize waiting times
    plt.hist(supermarket.waiting_times, bins=range(0, int(max(supermarket.waiting_times)) + 1, 1), alpha=0.7)
    plt.title('Customer Waiting Times')
    plt.xlabel('Waiting Time (minutes)')
    plt.ylabel('Frequency')
    plt.show()

if __name__ == "__main__":
    main()
