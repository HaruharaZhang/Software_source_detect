import requests
from prettytable import PrettyTable
from termcolor import colored
import csv
from datetime import datetime

# 常用软件源列表
software_sources = [
    {"name": "Docker 官方镜像", "url": "https://registry-1.docker.io/"},
    {"name": "Docker Hub", "url": "https://hub.docker.com/"},
    {"name": "Docker 官方网站", "url": "https://www.docker.com"},
    {"name": "Docker 阿里云镜像", "url": "https://cr.console.aliyun.com/"},
    {"name": "npm 官方源", "url": "https://registry.npmjs.org/"},
    {"name": "npm 淘宝镜像", "url": "https://registry.npmmirror.com/"},
    {"name": "Maven 中央仓库", "url": "https://repo1.maven.org/maven2/"},
    {"name": "Maven 阿里云镜像", "url": "https://maven.aliyun.com/repository/central"},
    {"name": "PyPI 官方源", "url": "https://pypi.org/simple/"},
    {"name": "PyPI 清华大学镜像", "url": "https://pypi.tuna.tsinghua.edu.cn/simple/"},
    {"name": "PyPI 豆瓣镜像", "url": "https://pypi.doubanio.com/simple/"},
    {"name": "Ubuntu 官方源", "url": "http://archive.ubuntu.com/ubuntu/"},
    {"name": "Ubuntu 阿里云镜像", "url": "http://mirrors.aliyun.com/ubuntu/"},
    {"name": "CentOS 官方源", "url": "http://mirror.centos.org/centos/"},
    {"name": "CentOS 网易镜像", "url": "http://mirrors.163.com/centos/"},
    {"name": "Alpine 官方源", "url": "http://dl-cdn.alpinelinux.org/alpine/"},
    {"name": "Alpine 阿里云镜像", "url": "http://mirrors.aliyun.com/alpine/"},
    {"name": "Fedora 官方源", "url": "https://download.fedoraproject.org/"},
    {"name": "Fedora 清华大学镜像", "url": "https://mirrors.tuna.tsinghua.edu.cn/fedora/"},
    {"name": "Arch Linux 官方源", "url": "https://archlinux.org/"},
    {"name": "Arch Linux 清华大学镜像", "url": "https://mirrors.tuna.tsinghua.edu.cn/archlinux/"},
    {"name": "Debian 官方源", "url": "http://deb.debian.org/debian/"},
    {"name": "Debian 中科大镜像", "url": "https://mirrors.ustc.edu.cn/debian/"},
    {"name": "Gentoo 官方源", "url": "http://distfiles.gentoo.org/"},
    {"name": "Gentoo 清华大学镜像", "url": "https://mirrors.tuna.tsinghua.edu.cn/gentoo/"},
    {"name": "OpenSUSE 官方源", "url": "http://download.opensuse.org/"},
    {"name": "OpenSUSE 阿里云镜像", "url": "http://mirrors.aliyun.com/opensuse/"},
    {"name": "Kali Linux 官方源", "url": "http://http.kali.org/kali/"},
    {"name": "Kali Linux 清华大学镜像", "url": "https://mirrors.tuna.tsinghua.edu.cn/kali/"},
    {"name": "Manjaro 官方源", "url": "https://manjaro.org/download/"},
    {"name": "Manjaro 清华大学镜像", "url": "https://mirrors.tuna.tsinghua.edu.cn/manjaro/"},
    {"name": "Linux Mint 官方源", "url": "http://packages.linuxmint.com/"},
    {"name": "Linux Mint 中科大镜像", "url": "https://mirrors.ustc.edu.cn/linuxmint/"},
    {"name": "Deepin 官方源", "url": "https://community-packages.deepin.com/deepin/"},
    {"name": "Deepin 清华大学镜像", "url": "https://mirrors.tuna.tsinghua.edu.cn/deepin/"},
    {"name": "FreeBSD 官方源", "url": "http://ftp.freebsd.org/pub/FreeBSD/"},
    {"name": "OpenBSD 官方源", "url": "http://ftp.openbsd.org/pub/OpenBSD/"},
    {"name": "OpenBSD 清华大学镜像", "url": "https://mirrors.tuna.tsinghua.edu.cn/OpenBSD/"},
    {"name": "CPAN 官方源", "url": "http://www.cpan.org/"},
    {"name": "CPAN 清华大学镜像", "url": "https://mirrors.tuna.tsinghua.edu.cn/CPAN/"},
    {"name": "CRAN 官方源", "url": "https://cran.r-project.org/"},
    {"name": "CRAN 中科大镜像", "url": "https://mirrors.ustc.edu.cn/CRAN/"},
    {"name": "CTAN 官方源", "url": "http://www.ctan.org/"},
    {"name": "CTAN 清华大学镜像", "url": "https://mirrors.tuna.tsinghua.edu.cn/CTAN/"},
    {"name": "RubyGems 官方源", "url": "https://rubygems.org/"},
    {"name": "RubyGems 清华大学镜像", "url": "https://mirrors.tuna.tsinghua.edu.cn/rubygems/"},
    {"name": "Homebrew 官方源", "url": "https://brew.sh/"},
    {"name": "Homebrew 清华大学镜像", "url": "https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/"},
    {"name": "Go Modules 官方代理", "url": "https://proxy.golang.org/"},
    {"name": "Go Modules 七牛云代理", "url": "https://goproxy.cn/"},
    {"name": "Go Modules 阿里云代理", "url": "https://mirrors.aliyun.com/goproxy/"},
    {"name": "Anaconda 官方源", "url": "https://repo.anaconda.com/pkgs/"},
    {"name": "Anaconda 清华大学镜像", "url": "https://mirrors.tuna.tsinghua.edu.cn/anaconda/"},
    {"name": "Python 官方发布", "url": "https://www.python.org/ftp/python/"},
    {"name": "Python 华为云镜像", "url": "https://mirrors.huaweicloud.com/python/"},
    {"name": "Node.js 官方发布", "url": "https://nodejs.org/dist/"},
    {"name": "Node.js 清华大学镜像", "url": "https://mirrors.tuna.tsinghua.edu.cn/nodejs-release/"},
    {"name": "Helm 官方发布", "url": "https://github.com/helm/helm/releases"},
    {"name": "Quay.io 官方镜像", "url": "https://quay.io/"},
]

def check_availability(sources):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }  # 模拟浏览器的 User-Agent
    table = PrettyTable()
    table.field_names = ["软件源名称", "URL", "响应状态", "可访问性"]
    inaccessible_urls = []  # 用于存储完全不可访问的网址
    report_data = []  # 用于存储报告数据

    for source in sources:
        try:
            response = requests.get(source["url"], headers=headers, timeout=5)  # 添加 headers
            if response.status_code == 200:
                accessible = "可访问"
                status = f"{response.status_code} OK"
            elif response.status_code == 404:
                accessible = "服务器可达，页面不存在"
                status = f"{response.status_code} Not Found"
            else:
                accessible = "不可访问"
                status = f"{response.status_code}"
                inaccessible_urls.append({"name": source["name"], "url": source["url"]})
        except requests.RequestException:
            accessible = "不可访问"
            status = "连接失败"
            inaccessible_urls.append({"name": source["name"], "url": source["url"]})

        # 添加到表格和报告数据
        table.add_row([source["name"], source["url"], status, accessible])
        report_data.append([source["name"], source["url"], status, accessible])

    print(table)

    # 输出完全不可访问的网址，一行一个
    if inaccessible_urls:
        print("\n完全不可访问的网址：")
        for url_data in inaccessible_urls:
            print(url_data["url"])

    # 生成 CSV 报告
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("software_sources.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        # 写入报告标题和时间
        writer.writerow(["软件源检测报告"])
        writer.writerow([f"时间：{timestamp}"])
        writer.writerow([])  # 空行
        # 写入表头
        writer.writerow(["软件源名称", "URL", "响应状态", "可访问性"])
        # 写入数据
        writer.writerows(report_data)
        # 写入完全不可访问的网址
        if inaccessible_urls:
            writer.writerow([])  # 空行
            writer.writerow(["完全不可访问的网址"])
            for url_data in inaccessible_urls:
                writer.writerow([url_data["name"], url_data["url"]])

if __name__ == "__main__":
    check_availability(software_sources)
