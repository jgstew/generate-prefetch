
import parse_prefetch

def prefetches_have_matching_hashes(prefetch_one, prefetch_two):
    """Compare the file size and hashes to make sure they match"""
    if 'file_size' in prefetch_one:
        parsed_prefetch_one = prefetch_one
    else:
        parsed_prefetch_one = parse_prefetch.parse_prefetch(prefetch_one)

    if 'file_size' in prefetch_two:
        parsed_prefetch_two = prefetch_two
    else:
        parsed_prefetch_two = parse_prefetch.parse_prefetch(prefetch_two)

    # ensure both prefetches have the required details
    if not ( ( parsed_prefetch_one.keys() >= {"file_size", "file_sha1"} ) and ( parsed_prefetch_two.keys() >= {"file_size", "file_sha1"} ) ):
        print("invalid prefetch")
        if ( ( parsed_prefetch_one.keys() >= {"file_size", "file_md5"} ) and ( parsed_prefetch_two.keys() >= {"file_size", "file_md5"} ) ):
            print("Both Have MD5 - Is this for comparison?")
        return False

    try:
        # file_size could be an int or a string, force convertion to int for comparison. 
        if int(parsed_prefetch_one['file_size']) == int(parsed_prefetch_two['file_size']):
            if parsed_prefetch_one['file_sha1'] == parsed_prefetch_two['file_sha1']:
                if ( ( parsed_prefetch_one.keys() >= {"file_sha256"} ) and ( parsed_prefetch_two.keys() >= {"file_sha256"} ) ):
                # NOTE: need to also check sha256 if present
                    if parsed_prefetch_one['file_sha256'] == parsed_prefetch_two['file_sha256']:
                        return True
                    else:
                        print("ERROR: file_sha256 doesn't match")
                        return False
                else:
                    print("Warning: file_sha256 is missing but size and sha1 match")
                    return True
            else:
                print("ERROR: file_sha1 doesn't match")
        else:
            print("ERROR: file_size doesn't match")
    except ValueError:
        print("ERROR: Invalid file_size")
        return False

    # catch all:
    return False


def main():
    """Only called if this script is run directly"""
    prefetch_dictionary_one = {
                'file_name': 'unzip.exe',
                'file_size': '167936',
                'file_sha1': 'e1652b058195db3f5f754b7ab430652ae04a50b8',
                'download_url': 'http://software.bigfix.com/download/redist/unzip-5.52.exe'
                }
    print( prefetches_have_matching_hashes(prefetch_dictionary_one, prefetch_dictionary_one) )

# if called directly, then run this example:
if __name__ == '__main__':
    main()
