import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

def extract_dates(inPath):
    with open(inPath) as f:
        lines = f.read().splitlines()
    days_list = []
    for l in lines:
        fields = l.split('_')
        y_diff =  int(fields[9]) -  int(fields[1])
        m_diff =  int(fields[10]) -  int(fields[2])
        d_diff =  int(fields[11]) -  int(fields[3])
        days_list.append(y_diff*365 + m_diff*30 + d_diff)
    print(sorted(days_list))
    print(sum(days_list)/len(days_list))
    # print(len(days_list))
    # panda_series = pd.Series(sorted(days_list))
    # # ax = panda_series.plot.hist(grid=False, bins=[1,3,7,15,30,60,120,4000], rwidth=0.9, color='red')
    # print(panda_series.value_counts( bins=[1,3,7,15,30,60,120,4000]))
    # return
    # plt.title('Commute Times for 1,000 Commuters')
    # ax.grid(False)
    # ax.set_yticks([])
    # bins_list = [0,1,3,7,15,30,60,120,4000]
    # ax = plt.hist(days_list, bins = bins_list)

    #legend
    line1 = plt.plot()

    width = 0.8
    counts = [17,15,7,18,26,31,27]
    binss = ['1', '[2-7]', '[8-15]', '[16-30]', '[31-60]', '[61-120]', '[121+]']
    # binss = ['1', '[2-5]', '[6-15]', '[16-25]', '[26-45]', '[45+]']
    # binss = ['0', '1', '5', '15', '25', '45', '75']
    # binss = [1,2,3,4,5,6,7]
    fig, ax = plt.subplots()
    # ax.grid(False)

    # ax.legend(['Average Days online\n50'])

    # line1 = ax.bar(binss, counts, width=width, color='red', edgecolor='0', linewidth=3, label="Average Days remained Online:\n                   50")
    line1 = ax.bar(binss, counts, width=width, color='lightgray', edgecolor='0', linewidth=3)

    ax.text(-0.5, 26.3, 'Days Online on average:\n\n                  99', 
    fontsize=10, style='oblique', fontweight='bold',
     bbox={'facecolor': 'none', 'edgecolor': '0','pad': 10})

    # first_legend = plt.legend(handles=[line1], loc='upper left')
    # plt.gca().add_artist(first_legend)
 
    plt.xlabel('Days Online', fontsize=12)
    plt.ylabel('No. malicious Extensions', fontsize=12)
    # plt.grid(axis='y', alpha=0.75)
    # plt.yscale('log')
    # plt.show()
    fig.set_size_inches(8, 4)
    plt.savefig('average_days.pdf', dpi=1000, bbox_inches = 'tight',
    pad_inches = 0.1)

def main():
    inPath = "text_files/found_clusters_results_2020_08_04.txt"
    extract_dates(inPath)

if __name__ == '__main__':
    main()
