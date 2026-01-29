from functions.get_files_info import get_files_info

print("Result for current directory:")
get_files_info("calculator", ".")
print("Result for 'pkg' directory:")
get_files_info("calculator", "pkg")
print("Result for '/bin' directory:")
get_files_info("calculator", "/bin")
print("Result for '../' directory:")
get_files_info("calculator", "../")